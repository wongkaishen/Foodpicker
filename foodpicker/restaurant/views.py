from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'homepage/core/home.html')

def restaurant(request):
    return render(request,'homepage/content/res.html')

def about(request):
    return render(request,'homepage/content/about.html')