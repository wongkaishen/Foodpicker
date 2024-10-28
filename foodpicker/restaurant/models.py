from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField("Restaurant Name", max_length=200)
    description = models.TextField(null=False,blank=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    time = models.TimeField("Working Hour")
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)

    def __str__(self):
        return self.name
