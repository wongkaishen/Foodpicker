from django.db import models
from geopy.distance import geodesic
from django.contrib.auth.models import User

class Restaurant(models.Model):
    id = models.BigAutoField(primary_key=True)  # Ensure auto-increment
    name = models.CharField("Restaurant Name", max_length=200)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    opentime = models.TimeField("Opening Hour")
    closetime = models.TimeField("Closing Hour")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # New fields for approval system
    approved = models.BooleanField(default=False)  # False means unapproved by default
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Track who submitted

    def __str__(self):
        return self.name

    def get_distance(self, user_location):
        """Calculate distance between user and restaurant."""
        if self.latitude and self.longitude:
            restaurant_coords = (self.latitude, self.longitude)
            return round(geodesic(user_location, restaurant_coords).km, 2)
        return None
