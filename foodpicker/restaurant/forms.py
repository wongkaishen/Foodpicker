from django import forms
from .models import Restaurant, Category
from django.core.validators import MinValueValidator, MaxValueValidator


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Restaurant Name"}
            ),
            "location": forms.Select(attrs={"class": "form-control"}),
            "category": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Price"}
            ),
            "time": forms.DateTimeInput(
                attrs={"class": "form-control", "placeholder": "Working Hour"}
            ),
            "rate": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Rating"}
            ),
            "latitude": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Latitude"}
            ),
            "longitude": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Longitude"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        location = cleaned_data.get("location")
        if Restaurant.objects.filter(name=name, location=location).exists():
            raise forms.ValidationError(
                "A restaurant with the same name and location already exists."
            )
        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Category Name"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("A Category with the same name already exists.")
        return name



