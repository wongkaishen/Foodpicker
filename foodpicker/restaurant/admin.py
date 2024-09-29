from django.contrib import admin
from .models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):  
    list_display = ("name",  "price", "time", "latitude","longtitude","description")


admin.site.register(Restaurant, RestaurantAdmin)

