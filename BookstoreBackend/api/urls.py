from django.urls import path
from .views.user_views import users_list,user_details,is_user_admin, manage_user, manage_admin, edit_user
from .views.product_views import all_products_details, product_details, products_by_category, product_categories, manage_product
from .views.cart_views import user_cart_items,  modify_cart_item
from .views.order_views import user_orders, products_in_order, delivered_orders, orders_not_delivered, add_order, update_order

urlpatterns = [
    
    path('users/', users_list, name='users_list'),  # List all users
    path('users/<int:userid>/', user_details, name='user_details_api'),
    path('users/<int:userid>/is_admin/', is_user_admin, name='is_user_admin'),
    path('users/add/', manage_user, name='add_user'),    # For adding a user (POST)
    path('users/updateordelete/<int:userid>/', manage_user, name='update_or_delete_users'),    # For updating or deleting a user (PUT, PATCH, DELETE)

    path('products/', all_products_details, name='all_products_details'),  # List all products
    path('products/<int:productid>/', product_details, name='product_details'),
    path('products/category/<str:category>/', products_by_category, name='products_by_category'),
    path('products/categories/', product_categories, name='product_categories'),
    path('products/add/', manage_product, name='add_product'),  # for adding new product
    path('products/updateordelete/<int:productid>/', manage_product, name='update_or_delete_products'),  # for update or delete

    path('users/<int:userid>/cart/', user_cart_items, name='user_cart_items'),  # Get the cart of a specific user
    path('users/<int:userid>/cart/<int:productid>/', modify_cart_item, name='modify_cart_item'),
     path('users/edit/<int:userid>/', edit_user, name='edit_user'),
    path('admins/add/', manage_admin, name='add_admin'),  # For adding an admin
    path('admins/updateorremove/<int:adminid>/', manage_admin, name='updateorremove'),  # For updating or removing an admin

    path('orders/users/<int:userid>/', user_orders, name='user_orders'), 
    path('orders/<int:orderid>/products/', products_in_order, name='products_in_order'),
    path('orders/delivered/', delivered_orders, name='delivered_orders'),
    path('orders/not_delivered/', orders_not_delivered, name='orders_not_delivered'),
    path('orders/add/', add_order, name='add_order'), #add order details and orderproduct details
    path('orders/<int:orderid>/', update_order, name='update_order'),
]
