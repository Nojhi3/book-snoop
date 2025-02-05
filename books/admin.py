from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Category, Review, Order, OrderItem

admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
