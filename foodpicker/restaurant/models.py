from django.db import models


# Create your models here.


class Location(models.Model):
    name = models.CharField("Location Name", max_length=200)
    address = models.CharField(max_length=200)
    zip_code = models.CharField("Zip Code", max_length=200)
    phone = models.CharField("Contact Phone", max_length=25)
    web = models.URLField("Web Address", max_length=200)
    email_address = models.EmailField("Email Address", max_length=200)

    def __str__(self):
        return self.name


class user(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField("User Email Address", max_length=200)

    def __str__(self):
        return self.first_name + "" + self.last_name


class Ratings(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    __empty__ = "Unknown"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    Name = models.CharField("Restaurant Name", max_length=200)
    Location = models.ForeignKey(
        Location, blank=True, null=True, on_delete=models.CASCADE
    )
    Category = models.ManyToManyField(
        Category,
        default="Non Categorized",
    )
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Time = models.TimeField(
        "Working Hour",
    )
    Rates = models.IntegerField(
        Ratings,
        null=True,
        blank=True,
    )
    Customer = models.ManyToManyField(user, blank=True,)


    def __str__(self):
        return self.Name
    
    
