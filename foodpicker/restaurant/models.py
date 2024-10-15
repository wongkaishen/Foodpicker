from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class ApprovedRestaurant(models.Model):
    name = models.CharField("Restaurant Name", max_length=200)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    time = models.TimeField("Working Hour")
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)

    def __str__(self):
        return self.name

    
class RestaurantSubmission(models.Model):
    name = models.CharField("Restaurant Name", max_length=200)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.TimeField("Working Hour")  # Adjust as needed
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)  # Track verification status

    def __str__(self):
        return self.name
    

