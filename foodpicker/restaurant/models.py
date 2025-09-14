from django.db import models
from geopy.distance import geodesic
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class ContactMessage(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    subject = models.CharField(_("Subject"), max_length=200)
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(_("Read"), default=False)
    
    class Meta:
        ordering = ['-created_at'] 
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
    
    def __str__(self):
        return f"{self.subject} - {self.name}"

class Restaurant(models.Model):
    PRICE_CHOICES = [
        ('$', 'Budget'),
        ('$$', 'Moderate'),
        ('$$$', 'Expensive'),
        ('$$$$', 'Fine Dining'),
    ]

    CUISINE_CHOICES = [
        ('ASIAN', 'Asian'),
        ('ITALIAN', 'Italian'),
        ('MEXICAN', 'Mexican'),
        ('AMERICAN', 'American'),
        ('INDIAN', 'Indian'),
        ('MEDITERRANEAN', 'Mediterranean'),
        ('FRENCH', 'French'),
        ('JAPANESE', 'Japanese'),
        ('CHINESE', 'Chinese'),
        ('THAI', 'Thai'),
        ('KOREAN', 'Korean'),
        ('VIETNAMESE', 'Vietnamese'),
        ('GREEK', 'Greek'),
        ('TURKISH', 'Turkish'),
        ('MIDDLE_EASTERN', 'Middle Eastern'),
        ('LATIN', 'Latin American'),
        ('AFRICAN', 'African'),
        ('SEAFOOD', 'Seafood'),
        ('VEGETARIAN', 'Vegetarian'),
        ('VEGAN', 'Vegan'),
        ('OTHER', 'Other'),
    ]

    ESTABLISHMENT_CHOICES = [
        ('RESTAURANT', 'Restaurant'),
        ('CAFE', 'Cafe'),
        ('BAR', 'Bar & Pub'),
        ('FAST_FOOD', 'Fast Food'),
        ('BAKERY', 'Bakery'),
        ('COFFEE_SHOP', 'Coffee Shop'),
        ('FOOD_TRUCK', 'Food Truck'),
        ('TAKEAWAY', 'Takeaway'),
        ('ICE_CREAM', 'Ice Cream Shop'),
        ('BUFFET', 'Buffet'),
        ('FINE_DINING', 'Fine Dining'),
        ('CASUAL_DINING', 'Casual Dining'),
        ('DELI', 'Deli'),
        ('JUICE_BAR', 'Juice Bar'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(_("Restaurant Name"), max_length=200)
    description = models.TextField(_("Description"))
    cuisine_type = models.CharField(_("Cuisine Type"), max_length=50, choices=CUISINE_CHOICES, default='OTHER')
    establishment_type = models.CharField(_("Establishment Type"), max_length=50, choices=ESTABLISHMENT_CHOICES, default='RESTAURANT')
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    website = models.URLField(_("Website"), blank=True)
    price_range = models.CharField(_("Price Range"), max_length=4, choices=PRICE_CHOICES, default='$$')
    average_rating = models.FloatField(
        _("Average Rating"),
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    opentime = models.TimeField(_("Opening Hour"))
    closetime = models.TimeField(_("Closing Hour"))
    delivery_available = models.BooleanField(_("Delivery Available"), default=False)
    takeout_available = models.BooleanField(_("Takeout Available"), default=False)
    latitude = models.FloatField(_("Latitude"), null=True, blank=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True)
    street_address = models.CharField(_("Street Address"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    state = models.CharField(_("State/Province"), max_length=100, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True)
    country = models.CharField(_("Country"), max_length=100, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(_("Approved"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.city})"

    def approve(self):
        """Mark the restaurant as approved and transfer to ApprovedRestaurant."""
        ApprovedRestaurant.objects.create(
            name=self.name,
            description=self.description,
            cuisine_type=self.cuisine_type,
            phone=self.phone,
            email=self.email,
            website=self.website,
            price_range=self.price_range,
            average_rating=self.average_rating,
            opentime=self.opentime,
            closetime=self.closetime,
            delivery_available=self.delivery_available,
            takeout_available=self.takeout_available,
            latitude=self.latitude,
            longitude=self.longitude,
            street_address=self.street_address,
            city=self.city,
            state=self.state,
            postal_code=self.postal_code,
            country=self.country,
            submitted_by=self.submitted_by,
        )
        self.delete()


class ApprovedRestaurant(models.Model):
    PRICE_CHOICES = Restaurant.PRICE_CHOICES
    CUISINE_CHOICES = Restaurant.CUISINE_CHOICES

    name = models.CharField(_("Restaurant Name"), max_length=200, db_index=True)
    description = models.TextField(_("Description"))
    cuisine_type = models.CharField(_("Cuisine Type"), max_length=50, choices=CUISINE_CHOICES, default='OTHER', db_index=True)
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    website = models.URLField(_("Website"), blank=True)
    price_range = models.CharField(_("Price Range"), max_length=4, choices=PRICE_CHOICES, default='$$', db_index=True)
    average_rating = models.FloatField(
        _("Average Rating"),
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        db_index=True,
    )
    opentime = models.TimeField(_("Opening Hour"))
    closetime = models.TimeField(_("Closing Hour"))
    delivery_available = models.BooleanField(_("Delivery Available"), default=False, db_index=True)
    takeout_available = models.BooleanField(_("Takeout Available"), default=False, db_index=True)
    latitude = models.FloatField(_("Latitude"), null=True, blank=True, db_index=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True, db_index=True)
    street_address = models.CharField(_("Street Address"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    state = models.CharField(_("State/Province"), max_length=100, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True)
    country = models.CharField(_("Country"), max_length=100, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Approved Restaurant")
        verbose_name_plural = _("Approved Restaurants")

    def __str__(self):
        return f"{self.name} ({self.city})"


class GooglePlacesRestaurant(models.Model):
    """Model to store restaurant data fetched from Google Places API"""
    
    # Google Places specific fields
    google_place_id = models.CharField(_("Google Place ID"), max_length=255, unique=True)
    name = models.CharField(_("Restaurant Name"), max_length=200)
    formatted_address = models.TextField(_("Formatted Address"), blank=True)
    
    # Location data
    latitude = models.FloatField(_("Latitude"), null=True, blank=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True)
    
    # Contact information
    phone = models.CharField(_("Phone Number"), max_length=50, blank=True)
    website = models.URLField(_("Website"), blank=True)
    google_url = models.URLField(_("Google Maps URL"), blank=True)
    
    # Restaurant details
    cuisine_type = models.CharField(_("Cuisine Type"), max_length=50, choices=Restaurant.CUISINE_CHOICES, default='OTHER')
    establishment_type = models.CharField(_("Establishment Type"), max_length=50, choices=Restaurant.ESTABLISHMENT_CHOICES, default='RESTAURANT')
    price_level = models.IntegerField(_("Price Level"), null=True, blank=True, help_text="0-4 scale from Google")
    price_range = models.CharField(_("Price Range"), max_length=4, choices=Restaurant.PRICE_CHOICES, default='$$')
    
    # Ratings and reviews
    rating = models.FloatField(
        _("Google Rating"),
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
    )
    user_ratings_total = models.IntegerField(_("Total Reviews"), default=0)
    
    # Operating hours
    opening_hours_text = models.TextField(_("Opening Hours"), blank=True, help_text="Weekday text from Google")
    is_open_now = models.BooleanField(_("Open Now"), null=True, blank=True)
    is_open_24_hours = models.BooleanField(_("Open 24 Hours"), default=False)
    
    # Service options
    delivery_available = models.BooleanField(_("Delivery Available"), default=False)
    takeout_available = models.BooleanField(_("Takeout Available"), default=False)
    
    # Business status
    business_status = models.CharField(_("Business Status"), max_length=50, default='OPERATIONAL')
    
    # Google Places types (stored as JSON)
    google_types = models.JSONField(_("Google Place Types"), default=list, blank=True)
    
    # Photo references (stored as JSON)
    photo_references = models.JSONField(_("Photo References"), default=list, blank=True)
    
    # Reviews data (stored as JSON)
    reviews_data = models.JSONField(_("Reviews Data"), default=list, blank=True)
    
    # Metadata
    last_updated_from_google = models.DateTimeField(_("Last Updated from Google"), auto_now=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    # Cache management
    cache_expires_at = models.DateTimeField(_("Cache Expires At"), null=True, blank=True)
    
    class Meta:
        ordering = ['-rating', '-user_ratings_total']
        verbose_name = _("Google Places Restaurant")
        verbose_name_plural = _("Google Places Restaurants")
        indexes = [
            models.Index(fields=['google_place_id']),
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['cuisine_type']),
            models.Index(fields=['establishment_type']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.name} (Google: {self.google_place_id[:20]}...)"
    
    def get_full_address(self):
        """Return the formatted address"""
        return self.formatted_address
    
    def get_cuisine_type_display_custom(self):
        """Get display name for cuisine type"""
        return dict(Restaurant.CUISINE_CHOICES).get(self.cuisine_type, self.cuisine_type)
    
    def get_photo_urls(self, api_key, max_width=800):
        """Generate photo URLs from photo references"""
        photo_urls = []
        for photo_ref in self.photo_references:
            if isinstance(photo_ref, dict) and 'photo_reference' in photo_ref:
                url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photo_reference={photo_ref['photo_reference']}&key={api_key}"
                photo_urls.append(url)
        return photo_urls
    
    def is_cache_valid(self):
        """Check if the cached data is still valid"""
        if not self.cache_expires_at:
            return False
        from django.utils import timezone
        return timezone.now() < self.cache_expires_at
    
    def set_cache_expiry(self, hours=24):
        """Set cache expiry time"""
        from django.utils import timezone
        from datetime import timedelta
        self.cache_expires_at = timezone.now() + timedelta(hours=hours)
