import json
import requests
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
from .models import Restaurant, ContactMessage, ApprovedRestaurant, GooglePlacesRestaurant
from django.utils import timezone
from datetime import timedelta
from .forms import RestaurantForm
from functools import wraps
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from math import cos, radians, sqrt, atan2, sin
# Enhanced categorization imports are now imported on-demand in functions
# from google_places_categories import categorize_google_place, get_comprehensive_search_strategies


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
def get_res_list(request):
    # Get filter parameters from request
    search_query = request.GET.get("search", "").strip()
    cuisine_filter = request.GET.get("cuisine", "")
    price_filter = request.GET.get("price", "")
    sort_by = request.GET.get("sort_by", "rating")
    delivery_filter = request.GET.get("delivery") == "true"
    takeout_filter = request.GET.get("takeout") == "true"

    # Start with all approved restaurants
    restaurants = ApprovedRestaurant.objects.all()

    # Apply search filter
    if search_query:
        restaurants = restaurants.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Apply cuisine filter
    if cuisine_filter:
        restaurants = restaurants.filter(cuisine_type=cuisine_filter)

    # Apply price filter
    if price_filter:
        restaurants = restaurants.filter(price_range=price_filter)

    # Apply delivery/takeout filters
    if delivery_filter:
        restaurants = restaurants.filter(delivery_available=True)
    if takeout_filter:
        restaurants = restaurants.filter(takeout_available=True)

    # Apply sorting
    sorting_options = {
        "rating": "-average_rating",  # Highest rating first
        "name": "name",  # Alphabetical order
        "price": "price_range",  # Lower price first
    }
    restaurants = restaurants.order_by(sorting_options.get(sort_by, "-average_rating"))

    # If it's an AJAX request, return JSON data
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        restaurant_data = [
            {
                "id": r.id,
                "name": r.name,
                "cuisine_type": r.get_cuisine_type_display(),
                "price_range": r.get_price_range_display(),
                "average_rating": r.average_rating,
                "description": r.description,
                "delivery_available": r.delivery_available,
                "takeout_available": r.takeout_available,
            }
            for r in restaurants
        ]
        return JsonResponse({"restaurants": restaurant_data})

    # Regular page load
    context = {
        "restaurants": restaurants,
        "title": "Restaurant",
        "price_choices": Restaurant.PRICE_CHOICES,
        "cuisine_choices": Restaurant.CUISINE_CHOICES,
        "establishment_choices": Restaurant.ESTABLISHMENT_CHOICES,
    }
    return render(request, "homepage/content/res.html", context)


@signup_required
def get_res_detail(request, id):
    """Get restaurant details from local database (existing functionality)"""
    restaurant = get_object_or_404(ApprovedRestaurant, id=id)
    return render(
        request, "homepage/content/restaurant_detail.html", {"restaurant": restaurant}
    )

def get_google_restaurant_detail(request, place_id):
    """Get restaurant details from Supabase cache or Google Places API"""
    try:
        # Get restaurant data (from cache or fresh from Google)
        restaurant, message = get_or_fetch_google_restaurant(place_id)
        
        if not restaurant:
            return render(request, 'homepage/content/restaurant_detail.html', {
                'error': message,
                'title': 'Restaurant Not Found'
            })
        
        # Get Google Maps API key for photo URLs
        api_key = settings.GOOGLE_MAPS_API_KEY
        
        # Generate photo URLs
        photos = []
        if restaurant.photo_references and api_key:
            photo_urls = restaurant.get_photo_urls(api_key, max_width=800)
            for i, url in enumerate(photo_urls):
                photos.append({
                    'url': url,
                    'width': 800,
                    'height': 600
                })
        
        # Format reviews
        reviews = []
        for review_data in restaurant.reviews_data:
            reviews.append({
                'author_name': review_data.get('author_name', 'Anonymous'),
                'rating': review_data.get('rating', 0),
                'text': review_data.get('text', ''),
                'time': review_data.get('time', 0),
                'profile_photo_url': review_data.get('profile_photo_url', '')
            })
        
        # Format opening hours
        opening_hours = {
            'open_now': restaurant.is_open_now,
            'weekday_text': restaurant.opening_hours_text.split('\n') if restaurant.opening_hours_text else [],
            'is_24_hours': restaurant.is_open_24_hours
        }
        
        # Create template-compatible object
        restaurant_data = {
            'google_place_id': restaurant.google_place_id,
            'name': restaurant.name,
            'formatted_address': restaurant.formatted_address,
            'phone': restaurant.phone,
            'website': restaurant.website,
            'latitude': restaurant.latitude,
            'longitude': restaurant.longitude,
            'rating': restaurant.rating,
            'user_ratings_total': restaurant.user_ratings_total,
            'price_level': restaurant.price_level,
            'cuisine_type': restaurant.cuisine_type,
            'establishment_type': restaurant.establishment_type,
            'types': restaurant.google_types,
            'business_status': restaurant.business_status,
            'photos': photos,
            'reviews': reviews,
            'opening_hours': opening_hours,
            'google_url': restaurant.google_url,
            
            # Template compatibility methods/properties
            'get_full_address': lambda: restaurant.formatted_address,
            'get_cuisine_type_display': restaurant.get_cuisine_type_display_custom(),
            'average_rating': restaurant.rating,
            'price_range': restaurant.price_range,
            'is_open_24_hours': restaurant.is_open_24_hours,
            'delivery_available': restaurant.delivery_available,
            'takeout_available': restaurant.takeout_available,
            'email': '',  # Google Places API doesn't provide email
            'description': f"A {restaurant.get_cuisine_type_display_custom().lower()} {restaurant.establishment_type.lower()} with {restaurant.user_ratings_total} reviews and a {restaurant.rating} star rating.",
            'opentime': None,
            'closetime': None,
            'image': {'url': photos[0]['url']} if photos else None,
        }
        
        context = {
            'restaurant': type('obj', (object,), restaurant_data),
            'title': f"{restaurant.name} - Restaurant Details",
            'is_google_data': True,
            'photos': photos,
            'reviews': reviews,
            'opening_hours': opening_hours,
            'data_source': message,  # Show where data came from
            'last_updated': restaurant.last_updated_from_google.strftime('%Y-%m-%d %H:%M:%S') if restaurant.last_updated_from_google else 'Unknown'
        }
        
        return render(request, 'homepage/content/restaurant_detail.html', context)
        
    except Exception as e:
        return render(request, 'homepage/content/restaurant_detail.html', {
            'error': f"Unexpected error: {str(e)}",
            'title': 'Error'
        })

def google_restaurant_test(request):
    """Test page to demonstrate Google restaurant detail functionality"""
    # Some sample Google Place IDs for testing (you can replace these with real ones)
    sample_places = [
        {
            'name': 'McDonald\'s KLCC',
            'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',  # Sample place ID (replace with real ones)
            'description': 'Fast food restaurant'
        },
        {
            'name': 'Starbucks Coffee',
            'place_id': 'ChIJrTLr-GyuEmsRBfy61i59si0',  # Sample place ID (replace with real ones)
            'description': 'Coffee shop'
        },
        {
            'name': 'KFC Restaurant',
            'place_id': 'ChIJ2_xOe_KuEmsRNBjVQs3X2Ps',  # Sample place ID (replace with real ones)
            'description': 'Fried chicken restaurant'
        }
    ]
    
    context = {
        'title': 'Google Restaurant Test',
        'sample_places': sample_places
    }
    
    return render(request, 'homepage/content/google_restaurant_test.html', context)



def get_res_map(request):
    """Render the restaurant map view with approved restaurant data."""
    cuisine_filter = request.GET.get("cuisine")
    price_filter = request.GET.get("price")
    
    restaurants = Restaurant.objects.filter(approved=True)  # Only approved restaurants
    
    if cuisine_filter:
        restaurants = restaurants.filter(cuisine_type=cuisine_filter)
    if price_filter:
        restaurants = restaurants.filter(price_range=price_filter)
    
    restaurants_json = json.dumps([
        {
            "id": r.id,
            "name": r.name,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "cuisine_type": r.get_cuisine_type_display(),
            "price_range": r.get_price_range_display(),
        }
        for r in restaurants if r.latitude and r.longitude
    ])
    
    context = {
        "restaurants_json": restaurants_json,
        'price_choices': Restaurant.PRICE_CHOICES,
        'cuisine_choices': Restaurant.CUISINE_CHOICES,
        'establishment_choices': Restaurant.ESTABLISHMENT_CHOICES,
        'title': 'Restaurant Map'
    }
    return render(request, "homepage/content/map.html", context)

def featured_restaurants_api(request):
    """API endpoint to fetch featured restaurants (top rated)."""
    try:
        # Get top 3 restaurants by rating that are approved
        restaurants = Restaurant.objects.filter(approved=True).order_by('-average_rating')[:3]
        
        # Format the restaurant data
        restaurant_data = []
        for ApprovedRestaurant in restaurants:
            restaurant_data.append({
                'id': ApprovedRestaurant.id,
                'name': ApprovedRestaurant.name,
                'cuisine_type': ApprovedRestaurant.get_cuisine_type_display(),
                'price_range': ApprovedRestaurant.price_range,
                'average_rating': ApprovedRestaurant.average_rating,
                'city': ApprovedRestaurant.city
            })
        
        return JsonResponse({'restaurants': restaurant_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def geocode_address(address):
    """Geocode an address using Google Maps Geocoding API."""
    api_key = settings.GOOGLE_MAPS_API_KEY
    if not api_key:
        return None, None
    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Geocoding failed: {data.get('status', 'Unknown error')}")
            return None, None
    except requests.RequestException as e:
        print(f"Error geocoding address: {e}")
        return None, None

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in kilometers.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Radius of Earth in kilometers
    earth_radius = 6371.0
    
    # Calculate the distance
    distance = earth_radius * c
    return distance

def restaurants_within_radius(request):
    """Return restaurants within the selected radius from the user's location."""
    try:
        user_lat = float(request.GET.get("latitude"))
        user_lon = float(request.GET.get("longitude"))
        radius = float(request.GET.get("radius"))  # in km
        cuisine_filter = request.GET.get("cuisine", "")
        price_filter = request.GET.get("price", "")

    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid parameters"}, status=400)

    user_location = (user_lat, user_lon)
    
    # Start with a base queryset and select only needed fields
    restaurants = ApprovedRestaurant.objects.only(
        'id', 'name', 'latitude', 'longitude', 
        'cuisine_type', 'price_range'
    )

    # Apply filters efficiently
    if cuisine_filter:
        restaurants = restaurants.filter(cuisine_type=cuisine_filter)
    if price_filter:
        restaurants = restaurants.filter(price_range=price_filter)

    # Calculate rough distance bounds to reduce the number of restaurants to check
    # 1 degree of latitude/longitude is approximately 111km at the equator
    lat_range = radius / 111.0
    lon_range = radius / (111.0 * abs(cos(radians(user_lat))))
    
    restaurants = restaurants.filter(
        latitude__range=(user_lat - lat_range, user_lat + lat_range),
        longitude__range=(user_lon - lon_range, user_lon + lon_range)
    )
    
    # Calculate exact distances and filter
    filtered_restaurants = []
    for r in restaurants:
        distance = calculate_distance(user_lat, user_lon, r.latitude, r.longitude)
        if distance <= radius:
            filtered_restaurants.append({
                "id": r.id,
                "name": r.name,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "cuisine_type": r.get_cuisine_type_display(),
                "price_range": r.get_price_range_display(),
                "distance_km": distance
            })
    
    # Sort by distance
    filtered_restaurants.sort(key=lambda x: x['distance_km'])

    return JsonResponse({
        "restaurants": filtered_restaurants[:50]  # Limit to 50 results for performance
    })

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
                messages.success(request, "Location Submitted Successfully ")
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
    restaurants = ApprovedRestaurant.objects.all()

    nearest = min(
        restaurants,
        key=lambda r: calculate_distance(user_lat, user_lon, r.latitude, r.longitude) if r.latitude and r.longitude else float('inf')
    )

    return JsonResponse({
        "name": nearest.name,
        "latitude": nearest.latitude,
        "longitude": nearest.longitude,
        "distance_km": calculate_distance(user_lat, user_lon, nearest.latitude, nearest.longitude),
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
            
            # Send a ticket/request email to the user
            ticket_subject = f"Your Ticket Request: {subject}"
            ticket_body = f"""
            Dear {name},
            
            Thank you for reaching out to us. We have received your message and will get back to you shortly.
            
            Here is a copy of your message:
            Subject: {subject}
            Message: {message}
            
            If you have any additional information to provide, feel free to reply to this email.
            
            Best regards,
            The Foodpicker Team
            """
            
            send_mail(
                ticket_subject,
                ticket_body,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't prevent the message from being saved
            print(f"Error sending email: {e}")
        
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

# The following functions have been replaced by the enhanced categorization system
# in google_places_categories.py. They are kept here for backward compatibility
# but are no longer used in the main google_places_restaurants function.

def categorize_establishment_type(place_types):
    """
    Categorize a Google Place into establishment types based on place_types.
    """
    if not place_types:
        return 'OTHER'
    
    place_types_lower = [pt.lower() for pt in place_types]
    place_types_str = ' '.join(place_types_lower)
    
    # Fast Food
    fast_food_types = ['fast_food', 'fast_food_restaurant', 'quick_service']
    fast_food_keywords = ['mcdonald', 'burger king', 'kfc', 'subway', 'pizza hut', 'domino', 'fast food']
    if any(t in place_types_lower for t in fast_food_types) or any(k in place_types_str for k in fast_food_keywords):
        return 'FAST_FOOD'
    
    # Cafe/Coffee Shop
    cafe_types = ['cafe', 'coffee_shop', 'coffee']
    cafe_keywords = ['cafe', 'coffee', 'espresso', 'starbucks', 'costa']
    if any(t in place_types_lower for t in cafe_types) or any(k in place_types_str for k in cafe_keywords):
        return 'CAFE'
    
    # Bar/Pub
    bar_types = ['bar', 'night_club', 'pub', 'liquor_store']
    bar_keywords = ['bar', 'pub', 'lounge', 'tavern', 'brewery', 'cocktail']
    if any(t in place_types_lower for t in bar_types) or any(k in place_types_str for k in bar_keywords):
        return 'BAR'
    
    # Bakery
    bakery_types = ['bakery', 'pastry_shop']
    bakery_keywords = ['bakery', 'pastry', 'bread', 'cake', 'donut', 'croissant']
    if any(t in place_types_lower for t in bakery_types) or any(k in place_types_str for k in bakery_keywords):
        return 'BAKERY'
    
    # Ice Cream
    ice_cream_types = ['ice_cream_shop', 'frozen_yogurt_shop']
    ice_cream_keywords = ['ice cream', 'gelato', 'frozen yogurt', 'sorbet']
    if any(t in place_types_lower for t in ice_cream_types) or any(k in place_types_str for k in ice_cream_keywords):
        return 'ICE_CREAM'
    
    # Takeaway/Delivery
    takeaway_types = ['meal_takeaway', 'meal_delivery', 'food_delivery']
    takeaway_keywords = ['takeaway', 'delivery', 'pickup', 'to go']
    if any(t in place_types_lower for t in takeaway_types) or any(k in place_types_str for k in takeaway_keywords):
        return 'TAKEAWAY'
    
    # Food Truck
    food_truck_keywords = ['food truck', 'mobile', 'street food']
    if any(k in place_types_str for k in food_truck_keywords):
        return 'FOOD_TRUCK'
    
    # Juice Bar
    juice_keywords = ['juice', 'smoothie', 'fresh juice']
    if any(k in place_types_str for k in juice_keywords):
        return 'JUICE_BAR'
    
    # Fine Dining
    fine_dining_types = ['fine_dining_restaurant', 'upscale_restaurant']
    fine_dining_keywords = ['fine dining', 'upscale', 'gourmet', 'michelin']
    if any(t in place_types_lower for t in fine_dining_types) or any(k in place_types_str for k in fine_dining_keywords):
        return 'FINE_DINING'
    
    # Buffet
    buffet_keywords = ['buffet', 'all you can eat', 'smorgasbord']
    if any(k in place_types_str for k in buffet_keywords):
        return 'BUFFET'
    
    # Deli
    deli_keywords = ['deli', 'delicatessen', 'sandwich shop']
    if any(k in place_types_str for k in deli_keywords):
        return 'DELI'
    
    # Default to restaurant for food establishments
    food_establishment_types = [
        'restaurant', 'food', 'establishment'
    ]
    if any(t in place_types_lower for t in food_establishment_types):
        return 'RESTAURANT'
    
    return 'OTHER'

def categorize_place_type(place_types, place_name=""):
    """
    Categorize Google Places API types into cuisine categories.
    Returns the most appropriate cuisine type based on place types and name.
    Now includes ALL food establishments with expanded categories.
    """
    if not place_types:
        return 'OTHER'
    
    # Debug logging
    print(f"Categorizing place: {place_name}")
    print(f"Place types: {place_types}")
    
    # Convert to lowercase for matching
    place_types_lower = [pt.lower() for pt in place_types]
    place_name_lower = place_name.lower() if place_name else ""
    
    # Combine place types and name for comprehensive searching
    search_text = ' '.join(place_types_lower + [place_name_lower])
    
    # Define mapping from Google Places types to our cuisine categories
    type_to_cuisine = {
        # Asian cuisine types - be more comprehensive
        'chinese_restaurant': 'CHINESE',
        'japanese_restaurant': 'JAPANESE', 
        'korean_restaurant': 'KOREAN',
        'thai_restaurant': 'THAI',
        'vietnamese_restaurant': 'VIETNAMESE',
        'asian_restaurant': 'ASIAN',
        'sushi_restaurant': 'JAPANESE',
        'ramen_restaurant': 'JAPANESE',
        'noodle_house': 'ASIAN',
        'dim_sum_restaurant': 'CHINESE',
        
        # Italian cuisine types
        'italian_restaurant': 'ITALIAN',
        'pizza': 'ITALIAN',
        'pizzeria': 'ITALIAN',
        
        # Mexican cuisine types
        'mexican_restaurant': 'MEXICAN',
        'taco_restaurant': 'MEXICAN',
        
        # American cuisine types
        'american_restaurant': 'AMERICAN',
        'hamburger_restaurant': 'AMERICAN',
        'steak_house': 'AMERICAN',
        'barbecue_restaurant': 'AMERICAN',
        'sandwich_shop': 'AMERICAN',
        'burger_restaurant': 'AMERICAN',
        
        # Indian cuisine types
        'indian_restaurant': 'INDIAN',
        'curry_restaurant': 'INDIAN',
        
        # Mediterranean cuisine types
        'middle_eastern_restaurant': 'MEDITERRANEAN',
        'mediterranean_restaurant': 'MEDITERRANEAN',
        'greek_restaurant': 'GREEK',
        'turkish_restaurant': 'TURKISH',
        'lebanese_restaurant': 'MEDITERRANEAN',
        
        # French cuisine
        'french_restaurant': 'FRENCH',
        
        # Seafood
        'seafood_restaurant': 'SEAFOOD',
    }
    
    # Check for specific restaurant types first
    for place_type in place_types_lower:
        if place_type in type_to_cuisine:
            result = type_to_cuisine[place_type]
            print(f"Direct type match: {place_type} -> {result}")
            return result
    
    # Enhanced keyword matching with cuisine-specific terms
    cuisine_keywords = {
        'CHINESE': ['chinese', 'dim sum', 'szechuan', 'cantonese', 'mandarin', 'peking', 'beijing', 'shanghai', 'hong kong', 'wonton', 'dumpling'],
        'JAPANESE': ['japanese', 'sushi', 'sashimi', 'ramen', 'udon', 'tempura', 'yakitori', 'hibachi', 'teriyaki', 'miso', 'sake', 'izakaya'],
        'KOREAN': ['korean', 'kimchi', 'bulgogi', 'bibimbap', 'galbi', 'seoul', 'bbq korean'],
        'THAI': ['thai', 'pad thai', 'tom yum', 'green curry', 'red curry', 'massaman', 'bangkok', 'som tam'],
        'VIETNAMESE': ['vietnamese', 'pho', 'banh mi', 'spring roll', 'saigon', 'ho chi minh'],
        'ASIAN': ['asian', 'oriental', 'noodle', 'rice bowl', 'stir fry', 'wok', 'asia'],
        'ITALIAN': ['italian', 'pizza', 'pasta', 'spaghetti', 'lasagna', 'risotto', 'gelato', 'trattoria', 'pizzeria', 'romano', 'tuscany'],
        'MEXICAN': ['mexican', 'taco', 'burrito', 'quesadilla', 'nachos', 'salsa', 'guacamole', 'tortilla', 'enchilada', 'mexico'],
        'AMERICAN': ['american', 'burger', 'hamburger', 'cheeseburger', 'steak', 'barbecue', 'bbq', 'grill', 'diner', 'usa'],
        'INDIAN': ['indian', 'curry', 'tandoori', 'biryani', 'naan', 'tikka', 'masala', 'dal', 'samosa', 'india'],
        'GREEK': ['greek', 'gyro', 'souvlaki', 'moussaka', 'feta', 'tzatziki', 'greece', 'mediterranean greek'],
        'TURKISH': ['turkish', 'kebab', 'doner', 'turkey', 'ottoman'],
        'MEDITERRANEAN': ['mediterranean', 'middle eastern', 'lebanese', 'hummus', 'falafel', 'shawarma', 'pita'],
        'FRENCH': ['french', 'bistro', 'brasserie', 'croissant', 'baguette', 'france', 'cafe french'],
        'SEAFOOD': ['seafood', 'fish', 'lobster', 'crab', 'shrimp', 'oyster', 'salmon', 'tuna'],
        'VEGETARIAN': ['vegetarian', 'vegan', 'plant based', 'veggie'],
        'VEGAN': ['vegan', 'plant based']
    }
    
    # Check keywords in search text
    for cuisine, keywords in cuisine_keywords.items():
        for keyword in keywords:
            if keyword in search_text:
                print(f"Keyword match: '{keyword}' in '{search_text}' -> {cuisine}")
                return cuisine
    
    # Check if it's a food establishment at all
    food_establishment_types = [
        'restaurant', 'cafe', 'bakery', 'bar', 'food', 'meal_takeaway', 
        'meal_delivery', 'fast_food_restaurant', 'seafood_restaurant', 
        'french_restaurant', 'fine_dining_restaurant', 'brunch_restaurant',
        'breakfast_restaurant', 'buffet_restaurant', 'family_restaurant',
        'ice_cream_shop', 'coffee_shop', 'tea_house', 'juice_shop',
        'sandwich_shop', 'pizza_restaurant', 'takeaway', 'food_court'
    ]
    
    place_types_lower = [pt.lower() for pt in place_types]
    is_food_establishment = any(t in place_types_lower for t in food_establishment_types)
    
    if is_food_establishment:
        print(f"Food establishment but no specific cuisine found -> OTHER")
        return 'OTHER'
    
    print(f"Not a food establishment -> OTHER")
    return 'OTHER'

def estimate_price_range(price_level):
    """
    Convert Google Places price_level to our price range format.
    Google Places price_level: 0 (free) to 4 (very expensive)
    """
    price_mapping = {
        0: '$',      # Free
        1: '$',      # Inexpensive  
        2: '$$',     # Moderate
        3: '$$$',    # Expensive
        4: '$$$$'    # Very Expensive
    }
    return price_mapping.get(price_level, '$$')  # Default to moderate

def google_places_restaurants(request):
    """
    Fetch all food establishments from Google Places API based on user location and distance.
    Returns categorized food places including restaurants, cafes, bars, bakeries, etc.
    """
    try:
        user_lat = float(request.GET.get("latitude"))
        user_lon = float(request.GET.get("longitude"))
        radius = min(float(request.GET.get("radius", 5)) * 1000, 50000)  # Convert km to meters, max 50km
        cuisine_filter = request.GET.get("cuisine", "")
        establishment_filter = request.GET.get("establishment", "")
        
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid parameters"}, status=400)

    # Get Google Maps API key from settings
    api_key = settings.GOOGLE_MAPS_API_KEY
    if not api_key:
        return JsonResponse({"error": "Google Maps API key not configured"}, status=500)

    # Google Places API endpoint for nearby search
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    # Use enhanced search strategies from the categorization module
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from google_places_categories import get_comprehensive_search_strategies
    search_strategies = get_comprehensive_search_strategies()
    
    all_places = []
    
    for strategy in search_strategies:
        params = {
            'location': f"{user_lat},{user_lon}",
            'radius': radius,
            'key': api_key
        }
        
        # Add the search parameter (either type or keyword)
        params.update(strategy)
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                all_places.extend(data.get('results', []))
                
        except requests.RequestException as e:
            print(f"Error fetching {strategy}: {e}")
            continue
    
    # Remove duplicates based on place_id
    unique_places = {}
    for place in all_places:
        place_id = place.get('place_id')
        if place_id and place_id not in unique_places:
            unique_places[place_id] = place
    
    restaurants = []
    filtered_out_count = 0
    
    for place in unique_places.values():
        # Skip if closed permanently
        if place.get('business_status') == 'CLOSED_PERMANENTLY':
            continue
            
        # Categorize the establishment using enhanced system
        place_types = place.get('types', [])
        place_name = place.get('name', '')
        
        # Use the enhanced categorization function
        from google_places_categories import categorize_google_place
        categorization_result = categorize_google_place(place)
        cuisine_type = categorization_result['cuisine']
        establishment_type = categorization_result['establishment_type']
        
        # Debug logging for categorization
        if (cuisine_filter and cuisine_filter != "") or (establishment_filter and establishment_filter != ""):
            print(f"Place: {place.get('name')}")
            print(f"  Types: {place_types}")
            print(f"  Cuisine: {cuisine_type}")
            print(f"  Establishment: {establishment_type}")
            print(f"  Cuisine Filter: {cuisine_filter}")
            print(f"  Establishment Filter: {establishment_filter}")
            print(f"  Cuisine Match: {cuisine_type == cuisine_filter if cuisine_filter else 'N/A'}")
            print(f"  Establishment Match: {establishment_type == establishment_filter if establishment_filter else 'N/A'}")
            print("---")
        
        # Apply filters if specified
        filter_pass = True
        
        # Apply cuisine filter
        if cuisine_filter and cuisine_filter != "":
            if cuisine_type != cuisine_filter:
                filter_pass = False
        
        # Apply establishment filter
        if establishment_filter and establishment_filter != "":
            if establishment_type != establishment_filter:
                filter_pass = False
        
        if not filter_pass:
            filtered_out_count += 1
            continue
        
        # Calculate distance
        place_lat = place['geometry']['location']['lat']
        place_lon = place['geometry']['location']['lng']
        distance = calculate_distance(user_lat, user_lon, place_lat, place_lon)
        
        # Get price level and rating
        price_level = place.get('price_level')
        price_range = estimate_price_range(price_level) if price_level is not None else '$$'
        
        restaurant_data = {
            'id': place.get('place_id'),  # Use place_id as unique identifier
            'name': place.get('name'),
            'latitude': place_lat,
            'longitude': place_lon,
            'cuisine_type': cuisine_type,
            'establishment_type': establishment_type,  # Use our categorized establishment type
            'price_range': price_range,
            'distance_km': distance,
            'rating': place.get('rating', 0),
            'user_ratings_total': place.get('user_ratings_total', 0),
            'vicinity': place.get('vicinity', ''),
            'is_open': place.get('opening_hours', {}).get('open_now', None),
            'google_place_id': place.get('place_id'),
            'photo_reference': place.get('photos', [{}])[0].get('photo_reference') if place.get('photos') else None,
            'place_types': place_types[:3],  # First 3 types for reference
            'debug_all_types': place_types  # For debugging
        }
        
        restaurants.append(restaurant_data)
    
    # Debug logging for filtering results
    if cuisine_filter and cuisine_filter != "":
        print(f"Filter applied: {cuisine_filter}")
        print(f"Places found matching filter: {len(restaurants)}")
        print(f"Places filtered out: {filtered_out_count}")
        print(f"Total unique places: {len(unique_places)}")
    
    # Sort by distance
    restaurants.sort(key=lambda x: x['distance_km'])
    
    # Group by cuisine type for statistics
    cuisine_counts = {}
    establishment_counts = {}
    
    for restaurant in restaurants:
        cuisine = restaurant['cuisine_type']
        cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
        
        est_type = restaurant['establishment_type']
        establishment_counts[est_type] = establishment_counts.get(est_type, 0) + 1
    
    return JsonResponse({
        'restaurants': restaurants[:1000],  # Increased limit for more variety
        'total_count': len(restaurants),
        'cuisine_breakdown': cuisine_counts,
        'establishment_breakdown': establishment_counts,
        'unique_places_found': len(unique_places),
        'filtered_out_count': filtered_out_count,
        'applied_cuisine_filter': cuisine_filter,
        'applied_establishment_filter': establishment_filter,
        'source': 'google_places_all_food'
    })

def save_google_place_to_supabase(place_data, categorization_result):
    """
    Save Google Places restaurant data to Supabase database
    """
    try:
        place_id = place_data.get('place_id')
        if not place_id:
            return None, "No place_id provided"
        
        # Check if restaurant already exists
        restaurant, created = GooglePlacesRestaurant.objects.get_or_create(
            google_place_id=place_id,
            defaults={}
        )
        
        # Update restaurant data
        restaurant.name = place_data.get('name', 'Unknown Restaurant')
        restaurant.formatted_address = place_data.get('formatted_address', '')
        
        # Location
        geometry = place_data.get('geometry', {}).get('location', {})
        restaurant.latitude = geometry.get('lat', 0)
        restaurant.longitude = geometry.get('lng', 0)
        
        # Contact info
        restaurant.phone = place_data.get('formatted_phone_number', '')
        restaurant.website = place_data.get('website', '')
        restaurant.google_url = place_data.get('url', '')
        
        # Restaurant categorization
        restaurant.cuisine_type = categorization_result.get('cuisine', 'OTHER')
        restaurant.establishment_type = categorization_result.get('establishment_type', 'RESTAURANT')
        
        # Pricing
        price_level = place_data.get('price_level')
        restaurant.price_level = price_level
        if price_level is not None:
            price_mapping = {0: '$', 1: '$', 2: '$$', 3: '$$$', 4: '$$$$'}
            restaurant.price_range = price_mapping.get(price_level, '$$')
        
        # Ratings
        restaurant.rating = place_data.get('rating', 0)
        restaurant.user_ratings_total = place_data.get('user_ratings_total', 0)
        
        # Opening hours
        opening_hours = place_data.get('opening_hours', {})
        if opening_hours.get('weekday_text'):
            restaurant.opening_hours_text = '\n'.join(opening_hours['weekday_text'])
        restaurant.is_open_now = opening_hours.get('open_now')
        
        # Check if open 24 hours
        if opening_hours.get('periods'):
            for period in opening_hours['periods']:
                if period.get('open') and not period.get('close'):
                    restaurant.is_open_24_hours = True
                    break
        
        # Service options
        place_types = place_data.get('types', [])
        restaurant.delivery_available = 'meal_delivery' in place_types
        restaurant.takeout_available = 'meal_takeaway' in place_types
        
        # Business status
        restaurant.business_status = place_data.get('business_status', 'OPERATIONAL')
        
        # Store Google types
        restaurant.google_types = place_types
        
        # Store photo references
        photos = place_data.get('photos', [])
        restaurant.photo_references = photos[:10]  # Store up to 10 photos
        
        # Store reviews
        reviews = place_data.get('reviews', [])
        restaurant.reviews_data = reviews[:5]  # Store up to 5 reviews
        
        # Set cache expiry (24 hours)
        restaurant.set_cache_expiry(24)
        
        # Save to Supabase
        restaurant.save()
        
        action = "Created" if created else "Updated"
        return restaurant, f"{action} restaurant '{restaurant.name}' in Supabase"
        
    except Exception as e:
        return None, f"Error saving to Supabase: {str(e)}"

def get_or_fetch_google_restaurant(place_id, force_refresh=False):
    """
    Get restaurant from Supabase cache or fetch from Google Places API
    """
    try:
        # Try to get from Supabase first
        if not force_refresh:
            try:
                restaurant = GooglePlacesRestaurant.objects.get(google_place_id=place_id)
                if restaurant.is_cache_valid():
                    return restaurant, "Retrieved from Supabase cache"
            except GooglePlacesRestaurant.DoesNotExist:
                pass
        
        # Fetch fresh data from Google Places API
        api_key = settings.GOOGLE_MAPS_API_KEY
        if not api_key:
            return None, "Google Maps API key not configured"
        
        # Google Places API call
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'fields': 'place_id,name,formatted_address,geometry,formatted_phone_number,website,opening_hours,price_level,rating,user_ratings_total,reviews,photos,types,business_status,url',
            'key': api_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'OK':
            return None, f"Google Places API error: {data.get('status')}"
        
        place_data = data.get('result', {})
        
        # Categorize the restaurant
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from google_places_categories import categorize_google_place
        categorization_result = categorize_google_place(place_data)
        
        # Save to Supabase
        restaurant, save_message = save_google_place_to_supabase(place_data, categorization_result)
        
        if restaurant:
            return restaurant, f"Fetched from Google and saved to Supabase: {save_message}"
        else:
            return None, save_message
            
    except Exception as e:
        return None, f"Error fetching restaurant: {str(e)}"
