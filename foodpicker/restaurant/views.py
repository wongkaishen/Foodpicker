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
from .models import Restaurant
from django.shortcuts import render, get_object_or_404
from .forms import RestaurantForm 


# Create your views here.
def home(request):
    context = {"title": "Home"}
    return render(request,"homepage/content/home.html",context,)


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try another username.")
            return redirect("res.home")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("res.home")

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters.")
            return redirect("res.home")

        if pass1 != pass2:
            messages.error(request, "Passwords did not match.")
            return redirect("res.home")

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect("res.home")

        # Create user
        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(
            request,
            "Your account has been successfully created. We have sent you a confirmation email; please confirm it to activate your account.",
        )

        # Send confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm Your Email @ Foodpicker - Login"
        message2 = render_to_string(
            "verification/email_confirmation.html",
            {
                "name": myuser.username,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
                "token": generate_token().make_token(myuser),
            },
        )

        # Rename the EmailMessage variable to avoid confusion
        confirmation_email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        confirmation_email.fail_silently = True
        confirmation_email.send()

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
    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants,
        "title": "Restaurant",
    }
    return render(request, "homepage/content/res.html", context)


def restaurant_detail(
    request, id
):  # this is for the restaurant detail when click into it
    restaurant = get_object_or_404(Restaurant, id=id)
    context = {
        "restaurant": restaurant,
        "title": restaurant.name,
    }
    return render(request, "homepage/content/restaurant_detail.html", context)


def all_restaurants_map(request):
    # Get all restaurants from the database
    restaurants = Restaurant.objects.all()

    # Convert restaurant queryset to a JSON-friendly format
    restaurants_json = json.dumps(
        list(restaurants.values("name", "description", "latitude", "longitude"))
    )

    # Render the template with the data
    return render(
        request, "homepage/content/map.html", {"restaurants_json": restaurants_json}
    )


def about(request):
    context = {"title": "About"}
    return render(request, "homepage/content/about.html", context)


def search(request):
    context = {"title": "Search"}
    return render(request, "homepage/content/search.html", context)


def map(request):
    context = {"title": "Map"}
    return render(request, "homepage/content/map.html", context)


def location_view(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data["latitude"]
            longitude = form.cleaned_data["longitude"]
            # Do something with the valid data (like saving it or processing)
            return render(
                request,
                "homepage/content/form_success.html",
                {"latitude": latitude, "longitude": longitude},
            )
    else:
        form = RestaurantForm()

    return render(request, "homepage/content/form.html", {"form": form})


def contact(request):
    context = {"title": "Contact"}
    return render(request, "homepage/content/contact.html", context)


def forgotpass(request):
    context = {"title": "Forgot Password"}
    return render(request, "homepage/accounts/forgotpass.html", context)
