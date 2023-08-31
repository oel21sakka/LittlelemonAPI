from django.contrib import admin
from .models import Category,MenuItem,Order,OrderItem,Cart,Booking

# Register your models here.
admin.site.register([Category,MenuItem,Order,OrderItem,Cart,Booking])
