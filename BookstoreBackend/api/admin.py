from django.contrib import admin
from .models import Users, Products, Orders, Carts, CartProducts, OrderProduct, Admin

# Register your models here
admin.site.register(Users)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Carts)
admin.site.register(CartProducts)
admin.site.register(OrderProduct)
admin.site.register(Admin)
