from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, "homepage/content/home.html", {"title": "Home"})


def restaurant(request):
    return render(request, "homepage/content/res.html", {"title": "Restaurant"})


def about(request):
    return render(request, "homepage/content/about.html", {"title": "About"})

def search(request):
    return render(request, "homepage/content/search.html", {"title": "Search"})


