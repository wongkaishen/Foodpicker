from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from base import settings
from django.core.mail import send_mail

# Create your views here.


# Create your views here.
def home(request):
    return render(request, "homepage/content/home.html", {"title": "Home"})


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! Please try another username"
            )
            return redirect("res.home")

        if User.objects.filter(email=email):
            messages.error(request, "Email already register!")
            return redirect("res.home")

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters")

        if pass1 != pass2:
            messages.error(request, "Password didn't match")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect("res.home")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(
            request,
            " Your Account has been successfully created. We have sent you a confirmation email, Please confirm your email in order to activate your account",
        )

        subject = "Welcome to Foodpicker -"
        message = (
            "Hello!"
            + myuser.username
            + "!! \n"
            + "Welcome to Foodpicker!! \n Thanks you for visiting our website \n We have also sent you a confirmation email, Please confirm your email address in order to activate your account. \n Thank you"
        )
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect("signin")

    return render(request, "homepage/accounts/signup.html", {"title": "Sign Up"})


from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass1")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect(
                "res.home"
            )  # or any other page you want to redirect after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("res.home")  # or to your login page with an error message
    else:
        return redirect("res.home")  # redirect to home if method is not POST


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully! ")
    return redirect("res.home")


def restaurant(request):
    return render(request, "homepage/content/res.html", {"title": "Restaurant"})


def about(request):
    return render(request, "homepage/content/about.html", {"title": "About"})


def search(request):
    return render(request, "homepage/content/search.html", {"title": "Search"})


def map(request):
    return render(request, "homepage/content/map.html", {"title": "Map"})


def form(request):
    return render(request, "homepage/content/form.html", {"title": "Restaurant Form"})


def contact(request):
    return render(request, "homepage/content/contact.html", {"title": "Contact"})
