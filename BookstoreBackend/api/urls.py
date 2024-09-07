from django.contrib import admin
from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products),
    path('cart/add/', views.add_to_cart),
]