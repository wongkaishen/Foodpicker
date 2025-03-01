from django.contrib import admin
from .models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):  
    list_display = ("name",  "price", "opentime","closetime", "latitude","longitude","description",
                    "street_address","city","state","postal_code","country","approved", "submitted_by")
    list_filter = ("approved",)  # Filter restaurants by approval status
    search_fields = ("name", "submitted_by__username")  # Search by restaurant name or user
    actions = ["approve_restaurants"]

    def approve_restaurants(self, request, queryset):
        """Approve selected restaurants"""
        queryset.update(approved=True)
    approve_restaurants.short_description = "Approve selected restaurants"


admin.site.register(Restaurant, RestaurantAdmin)

