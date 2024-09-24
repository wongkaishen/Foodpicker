from django.contrib import admin
from .models import Restaurant, Location, Category, user
from .forms import RestaurantForm, CategoryForm

class CategoryInline(admin.TabularInline):
    model = Restaurant.category.through
    extra = 0

class RestaurantAdmin(admin.ModelAdmin):
    form = RestaurantForm    
    list_display = ("name", "display_location", "display_categories", "price", "time", "rate","latitude","longitude")
    inlines = [CategoryInline]

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()]) if obj.category.exists() else "No Categories"

    def display_location(self, obj):
        return obj.location.name if obj.location else "No Location"

    display_categories.short_description = "Categories"
    display_location.short_description = "Location"

    
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
