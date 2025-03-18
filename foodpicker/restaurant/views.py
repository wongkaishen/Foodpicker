import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404 , render
from django.contrib.auth.models import User
from base import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from .models import Restaurant, ContactMessage
from .forms import RestaurantForm
from geopy.geocoders import Nominatim
from functools import wraps
from django.http import JsonResponse, HttpResponse
from geopy.distance import geodesic


# Create your views here.

def reset_pass(request):
    context = {"title":"Reset Password"}
    return render(request, "homepage/accounts/forgotpass.html", context)

def home(request):  # home view point
    context = {"title": "Home"}
    return render(
        request,
        "homepage/content/home.html",
        context,
    )


def signup(request):  # signup view
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(
            username=username
        ).exists():  # look for existance username
            messages.error(
                request, "Username already exists! Please try another username."
            )
            return redirect("signup")

        if User.objects.filter(email=email).exists():  # look for existance email
            messages.error(request, "Email already registered!")
            return redirect("signup")

        if len(username) > 15:  # username cannot more than 15 char
            messages.error(request, "Username must be under 15 characters.")
            return redirect("signup")

        if pass1 != pass2:  # look pass1 and pass2 match
            messages.error(request, "Passwords did not match.")
            return redirect("signup")

        if not username.isalnum():  # see username is alphanumeric
            messages.error(request, "Username must be alphanumeric!")
            return redirect("signup")

        # Create user, if all meet requirement
        myuser = User.objects.create_user(
            username=username, email=email, password=pass1
        )
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()  # save to database

        # send a message to home page after signup and require user to do confirmation
        messages.success(
            request,
            "Your account has been successfully created. We have sent you a confirmation email; please confirm it to activate your account.",
            "if you did not see the confirmation link, please check your junk folder.",
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

def signup_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signup')  # Redirect to the signup page
        return view_func(request, *args, **kwargs)
    return wrapper


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
            )  # or any other page to redirect after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("signup")  # or to your login page with an error message
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
        return redirect("signin")
    else:
        return render(request, "verification\activation_failed.html")

@signup_required
def get_res_list(
    request,
):  # used to show the restaurnt id or sort out the restaurant using id's
    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants,
        "title": "Restaurant",
    }
    return render(request, "homepage/content/res.html", context)

@signup_required
def get_res_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    return render(
        request, "homepage/content/restaurant_detail.html", {"restaurant": restaurant}
    )



def get_res_map(request):
    """Render the restaurant map view with approved restaurant data."""
    restaurants = Restaurant.objects.filter(approved=True)  # Only approved restaurants
    restaurants_json = json.dumps([
        {
            "id": r.id,
            "name": r.name,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "opentime": r.opentime.strftime("%H:%M:%S"),
            "closetime": r.closetime.strftime("%H:%M:%S"),
        }
        for r in restaurants if r.latitude and r.longitude
    ])
    
    return render(request, "homepage/content/map.html", {"restaurants_json": restaurants_json})

def featured_restaurants_api(request):
    """API endpoint to fetch featured restaurants (top rated)."""
    try:
        # Get top 3 restaurants by rating that are approved
        restaurants = Restaurant.objects.filter(approved=True).order_by('-average_rating')[:3]
        
        # Format the restaurant data
        restaurant_data = []
        for restaurant in restaurants:
            restaurant_data.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'cuisine_type': restaurant.get_cuisine_type_display(),
                'price_range': restaurant.price_range,
                'average_rating': restaurant.average_rating,
                'city': restaurant.city
            })
        
        return JsonResponse({'restaurants': restaurant_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def geocode_address(address):
    """Geocode an address using OpenStreetMap (Nominatim)."""
    geolocator = Nominatim(user_agent="restaurant_locator")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    return None, None

def restaurants_within_radius(request):
    """Return restaurants within the selected radius from the user's location."""
    try:
        user_lat = float(request.GET.get("latitude"))
        user_lon = float(request.GET.get("longitude"))
        radius = float(request.GET.get("radius"))  # in km
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid parameters"}, status=400)

    user_location = (user_lat, user_lon)
    restaurants = Restaurant.objects.all()
    
    filtered_restaurants = [
        {
            "id": r.id,
            "name": r.name,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "distance_km": geodesic(user_location, (r.latitude, r.longitude)).km
        }
        for r in restaurants if r.latitude and r.longitude and geodesic(user_location, (r.latitude, r.longitude)).km <= radius
    ]

    return JsonResponse({"restaurants": filtered_restaurants})

@signup_required
def location_view(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)

            # Assign the currently logged-in user
            restaurant.submitted_by = request.user
            restaurant.approved = False  # Mark as unapproved by default

            # If address is provided, attempt geocoding
            if all([
                form.cleaned_data["street_address"],
                form.cleaned_data["city"],
                form.cleaned_data["state"],
                form.cleaned_data["postal_code"],
                form.cleaned_data["country"],
            ]):
                address = f"{form.cleaned_data['street_address']}, {form.cleaned_data['city']}, {form.cleaned_data['state']}, {form.cleaned_data['postal_code']}, {form.cleaned_data['country']}"
                latitude, longitude = geocode_address(address)
                if latitude is not None and longitude is not None:
                    restaurant.latitude = latitude
                    restaurant.longitude = longitude
                else:
                    return render(
                        request,
                        "homepage/content/form_failed.html",
                        {"message": "Address could not be geocoded. Please check the address and try again."},
                    )

            restaurant.save()
            return render(
                request,
                "homepage/content/form_success.html",
                {"message": "Restaurant submitted for approval!"},
            )
    else:
        form = RestaurantForm()

    return render(request, "homepage/content/form.html", {"form": form})



@signup_required
def nearest_restaurant(request):
    """Find the nearest restaurant to the user's location."""
    user_lat = request.GET.get("latitude")
    user_lon = request.GET.get("longitude")
    
    if not user_lat or not user_lon:
        return JsonResponse({"error": "User location required"}, status=400)

    user_location = (float(user_lat), float(user_lon))
    restaurants = Restaurant.objects.all()

    nearest = min(
        restaurants,
        key=lambda r: geodesic(user_location, (r.latitude, r.longitude)).km if r.latitude and r.longitude else float('inf')
    )

    return JsonResponse({
        "name": nearest.name,
        "latitude": nearest.latitude,
        "longitude": nearest.longitude,
        "distance_km": nearest.get_distance(user_location),
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Create and save the contact message
        contact_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact_message.save()
        
        # Send notification email to admin
        try:
            admin_email = settings.EMAIL_HOST_USER
            email_subject = f'New Contact Message: {subject}'
            email_body = f"""
            You have received a new contact message from the website:
            
            From: {name} ({email})
            Subject: {subject}
            
            Message:
            {message}
            
            You can view this message in the admin panel.
            """
            
            send_mail(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [admin_email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't prevent the message from being saved
            print(f"Error sending notification email: {e}")
        
        # Return success response for AJAX requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Your message has been sent successfully! We will get back to you soon.'
            })
        
        # Add success message for non-AJAX requests
        messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        return redirect('contact')
        
    context = {"title": "Contact"}
    return render(request, "homepage/content/contact.html", context)


def about(request):
    context = {"title": "About"}
    return render(request, "homepage/content/about.html", context)


def search(request):
    context = {"title": "Search"}
    return render(request, "homepage/content/search.html", context)
