from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="res.home"),
    path('restaurant/',views.restaurant_list,name="res.res"),
    path('restaurant/<int:id>/', views.restaurant_detail, name='restaurant_detail'), #this is for future can see the detail for all the restaurant 
    path('about/',views.about,name="res.about"),   
    path('search/',views.search,name="res.search"),  
    path('map/',views.all_restaurants_map,name="res.map"),   
    path('contact/',views.contact,name="res.contact"), 
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('forgotpass',views.forgotpass,name="forgotpass"),
    path('form',views.location_view,name="res.form"),
    
]
