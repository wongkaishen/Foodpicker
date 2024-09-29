from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
        required=True,
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        required=True,
    )


class RestaurantForm(forms.Form):
    Restaurant_Name = forms.CharField(
        label="Please Enter your Restaurant Name",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Restaurant Name"}),
        required=True,
    )
    longtitude = forms.FloatField(
        label="Please Insert the Longtitude",
        min_value=-90,
        max_value=90,
        required=True,
        help_text="Enter a longitude value between -90 and 90"
    )
    latitude = forms.FloatField(
        label="Please Insert the Latitude",
        min_value=-180,
        max_value=180,
        required=True,
        help_text="Enter a latitude value between -180 and 180"
    )

    def clean_latitude(self):
        latitude = self.cleaned_data.get("latitude")
        if latitude < -180.0 or latitude > 180.0:
            raise ValidationError("Enter a latitude value between -180 and 180")
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get("longitude")
        if longitude < -90.0 or longitude > 90.0:
            raise ValidationError("Enter a longitude value between -90 and 90")
        return longitude
