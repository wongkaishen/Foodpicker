from django import forms
from django.core.exceptions import ValidationError
from .models import Restaurant


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


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'price', 'time', 'longitude', 'latitude']