from django.shortcuts import render
from django.http import HttpResponse
import folium
# Create your views here.


def home(request):
    return render(request, "homepage/content/home.html", {"title": "Home"})


def restaurant(request):
    return render(request, "homepage/content/res.html", {"title": "Restaurant"})


def about(request):
    return render(request, "homepage/content/about.html", {"title": "About"})


def search(request):
    return render(request, "homepage/content/search.html", {"title": "Search"})

def map(request):
    return render(request, "homepage/content/map.html",{"title": "Map"})

def resform(request):
    return render(request, "homepage\content\res_form.html",{"title": "Restaurant Form"})