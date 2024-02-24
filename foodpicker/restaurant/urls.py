from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="res.home"),
    path('restaurant/',views.restaurant,name="res.res"),
    path('about/',views.about,name="res.about"),   
    path('search/',views.search,name="res.search"),   

]