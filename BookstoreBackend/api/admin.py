from django.contrib import admin
from .models import Users, Products, Orders, Carts, Cartproducts, Orderproduct, Admin

# Register your models here
admin.site.register(Users)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Carts)
admin.site.register(Cartproducts)
admin.site.register(Orderproduct)
admin.site.register(Admin)
