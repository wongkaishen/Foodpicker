from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="res.home"),
    path('restaurant/',views.restaurant,name="res.res"),
    path('about/',views.about,name="res.about"),   
    path('search/',views.search,name="res.search"),  
    path('map/',views.map,name="res.map"),   
    path('restaurant_form/',views.form,name="res.form"),   
    path('contact/',views.contact,name="res.contact"), 
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('forgotpass',views.forgotpass,name="forgotpass"),
]
