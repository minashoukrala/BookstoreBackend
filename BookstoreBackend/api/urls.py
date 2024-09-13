from django.urls import path
from .views.user_views import user_list, user_detail
from .views.product_views import product_list, product_detail
from .views.cart_views import view_cart
from .views.order_views import order_list, order_detail
from .views.auth_views import signup, login, test_token

urlpatterns = [
    path('users/', user_list, name='user_list'),  # List all users
    path('users/<int:user_id>/', user_detail, name='user_detail'),  # Get a specific user by ID

    path('products/', product_list, name='product_list'),  # List all products
    path('products/<int:product_id>/', product_detail, name='product_detail'),  # Get a specific product by ID

    path('cart/<int:user_id>/', view_cart, name='view_cart'),  # Get the cart of a specific user

    path('orders/<int:user_id>/', order_list, name='order_list'),  # List all orders for a user
    path('orders/detail/<int:order_id>/', order_detail, name='order_detail'),  # Get a specific order by ID

    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('test_token/', test_token, name='test_token'),
]
