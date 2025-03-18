from django.db import models
from geopy.distance import geodesic
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

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
        ('OTHER', 'Other'),
    ]

    # Basic Information
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(_("Restaurant Name"), max_length=200)
    description = models.TextField(_("Description"), help_text=_("Detailed description of the restaurant"))
    cuisine_type = models.CharField(_("Cuisine Type"), max_length=50, choices=CUISINE_CHOICES, default='OTHER')
    
    # Contact Information
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    website = models.URLField(_("Website"), blank=True)
    
    # Business Information
    price_range = models.CharField(_("Price Range"), max_length=4, choices=PRICE_CHOICES, default='$$')
    average_rating = models.FloatField(_("Average Rating"), 
                                     validators=[MinValueValidator(0), MaxValueValidator(5)],
                                     default=0)
    opentime = models.TimeField(_("Opening Hour"))
    closetime = models.TimeField(_("Closing Hour"))
    delivery_available = models.BooleanField(_("Delivery Available"), default=False)
    takeout_available = models.BooleanField(_("Takeout Available"), default=False)
    
    # Location Information
    latitude = models.FloatField(_("Latitude"), null=True, blank=True)
    longitude = models.FloatField(_("Longitude"), null=True, blank=True)
    street_address = models.CharField(_("Street Address"), max_length=255, blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True)
    state = models.CharField(_("State/Province"), max_length=100, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True)
    country = models.CharField(_("Country"), max_length=100, blank=True)
    
    # Meta Information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(_("Active"), default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Restaurant")
        verbose_name_plural = _("Restaurants")

    def __str__(self):
        return f"{self.name} ({self.city})"

    def get_distance(self, user_location):
        """Calculate distance between user and restaurant."""
        if self.latitude and self.longitude:
            restaurant_coords = (self.latitude, self.longitude)
            return round(geodesic(user_location, restaurant_coords).km, 2)
        return None

    def get_full_address(self):
        """Returns the full address as a formatted string."""
        address_parts = filter(None, [
            self.street_address,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ])
        return ", ".join(address_parts)

    @property
    def is_open_24_hours(self):
        """Check if restaurant is open 24 hours."""
        return self.opentime == self.closetime
