from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Restaurant

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class RestaurantSerializer(serializers.ModelSerializer):
    submitted_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'description', 'price', 'opentime', 'closetime',
            'latitude', 'longitude', 'street_address', 'city', 'state',
            'postal_code', 'country', 'approved', 'submitted_by'
        ) 