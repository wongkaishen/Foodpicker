from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class user(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField("User Email Address", max_length=200)

    def __str__(self):
        return self.first_name + "" + self.last_name


class Location(models.Model):
    name = models.CharField("Location Name", max_length=200)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(
        "Zip Code",
        max_length=200,
        null=True,
        blank=True,
    )
    phone = models.CharField(
        "Contact Phone",
        max_length=25,
        null=True,
        blank=True,
    )
    web = models.URLField(
        "Web Address",
        max_length=200,
        blank=True,
    )
    email_address = models.EmailField(
        "Email Address",
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField("Restaurant Name", max_length=200)
    location = models.ForeignKey(
        Location, blank=True, null=True, on_delete=models.CASCADE
    )
    category = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    time = models.TimeField("Working Hour")
    rate = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
    )
    customer = models.ManyToManyField(user, blank=True)
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)

    def save(self, *args, **kwargs):
        existing_restaurant = Restaurant.objects.filter(
            name=self.name, location=self.location
        ).exists()
        if existing_restaurant:
            return

        super().save(*args, **kwargs)

        self.category.set(self.category.all())

    def __str__(self):
        return self.name



