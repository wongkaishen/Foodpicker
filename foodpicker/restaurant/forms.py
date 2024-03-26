from django import forms
from .models import Restaurant
from .models import Category
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField()

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = "__all__"

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

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("A Category with the same name already exists.")
        return name


class CaptchaForm(forms.Form):
    captcha_field = CaptchaField()



