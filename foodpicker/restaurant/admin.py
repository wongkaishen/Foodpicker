from django.contrib import admin
from .models import Restaurant
from .models import Location
from .models import Category
from .models import user
from .forms import RestaurantForm
from .forms import CategoryForm

# Register your models here.


class RestaurantAdmin(admin.ModelAdmin):
    form = RestaurantForm    
    list_display = ("name", "location", "display_categories", "price", "time", "rate")

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])

    display_categories.short_description = "Categories"

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "zip_code", "phone", "web", "email_address")


class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(user, UserAdmin)
