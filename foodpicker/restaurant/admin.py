from django.contrib import admin
from .models import Restaurant
from .models import Location
from .models import Category
from .models import Ratings
from .models import user

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Ratings)
admin.site.register(user)
