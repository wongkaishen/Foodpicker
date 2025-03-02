from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from django.contrib.auth import views as auth_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'api/restaurants', views.RestaurantViewSet)

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    path('api/auth/user/', views.get_auth_user, name='auth_user'),
    path('api/csrf/', views.get_csrf_token, name='csrf_token'),
    path('api/verify-email/', views.verify_email, name='verify_email'),
    path('api/restaurants-within-radius/', views.api_restaurants_within_radius, name='api_restaurants_within_radius'),
    path('api/nearest-restaurant/', views.api_nearest_restaurant, name='api_nearest_restaurant'),
    
    # Existing URLs
    path("login/", auth_views.LoginView.as_view(template_name="accounts/signin.html"), name="login"),
    path('',views.home,name="res.home"),#redirect to home
    path('about/',views.about,name="res.about"),   #redirect to about page
    path('search/',views.search,name="res.search"),  #redirect to search page
    path('contact/',views.contact,name="res.contact"), #redirect to contact page
    path('signup',views.signup,name="signup"),#redirect to signup page
    path('signin',views.signin,name="signin"),#redirect home after signin or signup
    path('signout',views.signout,name="signout"),#redirect home after signout
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'), #redirect to home after verification
    path('form',views.location_view,name="res.form"), #redirect to form
    path('restaurant/',views.get_res_list,name="res.res"), #for the restaurant list
    path('restaurant/<int:id>/', views.get_res_detail, name='restaurant_detail'), #for the restaurant detail id
    path('map/',views.get_res_map,name="res.map"),   #for the whole map view of the restaurant
    path('password_reset/',views.reset_pass,name="resetpass"), 
    path('restaurants_within_radius/', views.restaurants_within_radius, name="restaurants_within_radius"),

]
