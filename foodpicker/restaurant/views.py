import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from base import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from .models import ApprovedRestaurant , RestaurantSubmission
from django.shortcuts import render, get_object_or_404
from .forms import RestaurantForm


# Create your views here.


# Create your views here.
def home(request):
    context = {"title": "Home"}
    return render(request, "homepage/content/home.html", context)


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! Please try another username"
            )
            return redirect("res.home")

        if User.objects.filter(email=email):
            messages.error(request, "Email already register!")
            return redirect("res.home")

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters")

        if pass1 != pass2:
            messages.error(request, "Password didn't match")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect("res.home")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(
            request,
            " Your Account has been successfully created. We have sent you a confirmation email, Please confirm your email in order to activate your account",
        )

        current_site = get_current_site(request)
        email_subject = "Confirm Your Email @ Foodpicker - Login"
        message2 = render_to_string(
            "verification\email_confirmation.html",
            {
                "name": myuser.username,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
                "token": generate_token().make_token(myuser),
            },
        )
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect("signin")

    context = {"title": "Sign Up"}

    return render(request, "homepage/accounts/signup.html", context)


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass1")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect(
                "res.home"
            )  # or any other page you want to redirect after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("res.home")  # or to your login page with an error message
    else:
        return redirect("res.home")  # redirect to home if method is not POST


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully! ")
    return redirect("res.home")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token().check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "You have successfully comfirmed your account")
        return redirect("res.home")
    else:
        return render(request, "verification\activation_failed.html")


def restaurant_list(
    request,
):  # used to show the restaurnt id or sort out the restaurant using id's
    restaurants = ApprovedRestaurant.objects.all()
    context = {
        "restaurants": restaurants,
        "title": "Restaurant",
    }
    return render(request, "homepage/content/res.html", context)


def restaurant_detail(
    request, id
):  # this is for the restaurant detail when click into it
    restaurant = get_object_or_404(ApprovedRestaurant, id=id)
    context = {
        "restaurant": restaurant,
        "title": restaurant.name,
    }
    return render(request, "homepage/content/restaurant_detail.html", context)


def all_restaurants_map(request):
    # Get all restaurants from the database
    restaurants = ApprovedRestaurant.objects.all()

    # Convert restaurant queryset to a JSON-friendly format
    restaurants_json = json.dumps(
        list(restaurants.values("name", "description", "latitude", "longitude"))
    )

    # Render the template with the data
    return render(
        request, "homepage/content/map.html", {"restaurants_json": restaurants_json}
    )


def Res_request(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"homepage\content\submission_success.html",)
    else:
        form = RestaurantForm()

    return render(request, "homepage/content/form.html", {"form": form})

def admin_verify_restaurants(request):
    # Fetch unverified restaurant submissions
    submissions = RestaurantSubmission.objects.filter(is_verified=False)
    
    if request.method == 'POST':
        for submission in submissions:
            if f'approve_{submission.id}' in request.POST:
                # Move to approved restaurant model
                ApprovedRestaurant.objects.create(
                    name=submission.name,
                    description=submission.description,
                    price=submission.price,
                    time=submission.time,
                    longitude=submission.longitude,
                    latitude=submission.latitude,
                )
                submission.is_verified = True  # Mark as verified
                submission.save()  # Save submission status

            elif f'disapprove_{submission.id}' in request.POST:
                submission.is_verified = True  # Mark as verified (optional)
                submission.save()  # Save submission status

        return redirect('admin_verify')  # Redirect back to this page
    
    context = {
        'submissions': submissions,
        'no_submissions': not submissions.exists(),  # Check if there are no submissions
    }

    return render(request, 'homepage/content/res_verify.html', context)

def submission_success_view(request):
    return render(request, 'homepage\content\submission_success.html')  # Create this template




def contact(request):
    context = {"title": "Contact"}
    return render(request, "homepage/content/contact.html", context)


def forgotpass(request):
    context = {"title": "Forgot Password"}
    return render(request, "homepage/accounts/forgotpass.html", context)


def about(request):
    context = {"title": "About"}
    return render(request, "homepage/content/about.html", context)


def search(request):
    context = {"title": "Search"}
    return render(request, "homepage/content/search.html", context)


def map(request):
    context = {"title": "Map"}
    return render(request, "homepage/content/map.html", context)
