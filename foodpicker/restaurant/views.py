import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404 , render
from django.contrib.auth.models import User
from base import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from .models import Restaurant
from .forms import RestaurantForm
from geopy.geocoders import Nominatim
from functools import wraps
from django.http import JsonResponse
from geopy.distance import geodesic
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import RestaurantSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.middleware.csrf import get_token


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


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_protect
def signup(request):  # signup view
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

        # Validation checks
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "success": False,
                "message": "Username already exists! Please try another username."
            }, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "success": False,
                "message": "Email already registered!"
            }, status=400)

        if len(username) > 15:
            return JsonResponse({
                "success": False,
                "message": "Username must be under 15 characters."
            }, status=400)

        if pass1 != pass2:
            return JsonResponse({
                "success": False,
                "message": "Passwords did not match."
            }, status=400)

        if not username.isalnum():
            return JsonResponse({
                "success": False,
                "message": "Username must be alphanumeric!"
            }, status=400)

        try:
            # Create user
            myuser = User.objects.create_user(
                username=username, email=email, password=pass1
            )
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()

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

            confirmation_email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            confirmation_email.fail_silently = True
            confirmation_email.send()

            return JsonResponse({
                "success": True,
                "message": "Account created successfully! Please check your email for verification."
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=500)

    return JsonResponse({
        "success": True,
        "csrftoken": get_token(request)
    })

def signup_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signup')  # Redirect to the signup page
        return view_func(request, *args, **kwargs)
    return wrapper


@csrf_protect
def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass1")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                return JsonResponse({
                    "success": False,
                    "message": "Please verify your email before logging in."
                }, status=400)
            
            login(request, user)
            return JsonResponse({
                "success": True,
                "message": f"Welcome {user.username}!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "Invalid username or password."
            }, status=400)

    return JsonResponse({
        "success": True,
        "csrftoken": get_token(request)
    })


@csrf_protect
def signout(request):
    logout(request)
    return JsonResponse({
        "success": True,
        "message": "Logged Out Successfully!"
    })


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
        messages.success(request, "Your account has been successfully activated!")
        return redirect("res.home")  # Redirect to home page
    else:
        messages.error(request, "Activation failed! Please try again.")
        return redirect("signin")  # Redirect to signin page if activation fails

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
    context = {"title": "Contact"}
    return render(request, "homepage/content/contact.html", context)


def about(request):
    context = {"title": "About"}
    return render(request, "homepage/content/about.html", context)


def search(request):
    context = {"title": "Search"}
    return render(request, "homepage/content/search.html", context)

# API Views
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.filter(approved=True)
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)

@api_view(['GET'])
def api_restaurants_within_radius(request):
    """API endpoint for restaurants within radius"""
    try:
        user_lat = float(request.GET.get("latitude"))
        user_lon = float(request.GET.get("longitude"))
        radius = float(request.GET.get("radius"))  # in km
    except (TypeError, ValueError):
        return Response({"error": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)

    user_location = (user_lat, user_lon)
    restaurants = Restaurant.objects.filter(approved=True)
    
    filtered_restaurants = [
        restaurant for restaurant in restaurants
        if restaurant.latitude and restaurant.longitude
        and geodesic(user_location, (restaurant.latitude, restaurant.longitude)).km <= radius
    ]

    serializer = RestaurantSerializer(filtered_restaurants, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_nearest_restaurant(request):
    """API endpoint for finding nearest restaurant"""
    try:
        user_lat = float(request.GET.get("latitude"))
        user_lon = float(request.GET.get("longitude"))
    except (TypeError, ValueError):
        return Response({"error": "Invalid parameters"}, status=status.HTTP_400_BAD_REQUEST)

    user_location = (user_lat, user_lon)
    restaurants = Restaurant.objects.filter(approved=True)

    if not restaurants:
        return Response({"error": "No restaurants found"}, status=status.HTTP_404_NOT_FOUND)

    nearest = min(
        restaurants,
        key=lambda r: geodesic(user_location, (r.latitude, r.longitude)).km if r.latitude and r.longitude else float('inf')
    )

    serializer = RestaurantSerializer(nearest)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_auth_user(request):
    if request.user.is_authenticated:
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        })
    return Response({'user': None})

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    try:
        uid = request.data.get('uid')
        token = request.data.get('token')
        
        if not uid or not token:
            return Response({
                'success': False,
                'message': 'Invalid verification link'
            }, status=status.HTTP_400_BAD_REQUEST)

        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
        
        if user is not None and generate_token().check_token(user, token):
            if user.is_active:
                return Response({
                    'success': False,
                    'message': 'Account is already verified'
                })
                
            user.is_active = True
            user.save()
            login(request, user)
            return Response({
                'success': True,
                'message': 'Email verified successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid verification link'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        return Response({
            'success': False,
            'message': 'Invalid verification link'
        }, status=status.HTTP_400_BAD_REQUEST)
