from django.contrib import admin
from .models import RestaurantSubmission, ApprovedRestaurant


class RestaurantSubmissionAdmin(admin.ModelAdmin):  
    list_display = ("name",  "price", "time", "latitude","longitude","description","submitted_at","'is_verified'")



admin.site.register(RestaurantSubmission)
admin.site.register(ApprovedRestaurant)

