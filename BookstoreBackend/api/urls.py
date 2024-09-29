from django.urls import path, include
from .views.user_views import users_list,user_details,is_user_admin, edit_user_info, user_status
from .views.product_views import all_products_details, product_details, products_by_category, products_by_category, search_products_by_user_input, add_product, update_product, delete_product, available_or_requestable_products, ProductListView, add_product_categories, delete_related_product_categories
from .views.cart_views import user_cart_items, modify_cart_item_quantity, add_item_to_cart, delete_cart_item
from .views.order_views import products_in_order, add_order, update_order, user_orders_with_products,get_all_orders,get_user_orders, get_orders_by_status
from .views.auth import RegisterView, LoginView, LogoutView, CustomPasswordResetView, CustomPasswordResetConfirmView
from rest_framework.authtoken.views import obtain_auth_token
from .views.catergories import add_category, all_categories, update_category 


urlpatterns = [
    
    path('users/', users_list, name='users_list'),  # List all users
    path('user_details/', user_details, name='user_details_api'),
    path('users/<int:userid>/is_admin/', is_user_admin, name='is_user_admin'),
    path('users/edit/', edit_user_info, name='edit_user_info'),
    path('users/status/', user_status, name='status'),

    path('products/admin/', all_products_details, name='all_products_details'),  # List all products
    path('products/available-or-requestable/', available_or_requestable_products, name='available_or_requestable_products'),
    #path('products/category/<int:categoryid>/available-or-requestable/', products_by_category_with_quantity_or_requestable, name='products_by_category_with_quantity_or_requestable'),
    path('products/<int:productid>/', product_details, name='product_details'),
    path('products/category/admin/<int:category_id>/', products_by_category, name='products_by_category'),
    path('products/categories/', products_by_category , name='product_categories'),
    path('products/search/', search_products_by_user_input, name='search_products_by_user_input'), #search
    path('products/add/', add_product, name='add_product'),  
    path('products/<int:productid>/add/', add_product_categories, name='add_product'),  
    path('products/update/<int:productid>/', update_product, name='update_product'),# URL pattern for updating a product
    path('products/delete/<int:productid>/', delete_product, name='delete_product'),# URL pattern for deleting a product
    path('products/delete_related_categories/<int:productid>/', delete_related_product_categories, name='delete-related-product-categories'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/category/<int:category_id>/', ProductListView.as_view(), name='product-list-by-category'),

    path('users/cart/', user_cart_items, name='user_cart_items'),  # Get the cart of a specific user
    
    path('cart/delete/', delete_cart_item, name='delete_cart_item'),# URL pattern for deleting an item from cart
    path('cart/modify/', modify_cart_item_quantity, name='modify_cart_item_quantity'), # URL pattern for modifying product quantity in cart
    path('cart/add/', add_item_to_cart, name='add_item_to_cart'),   # URL pattern for adding items to cart

    path('orders/user/<int:userid>/', user_orders_with_products, name='user_orders_with_products'),
    path('orders/user/', get_user_orders, name='user_orders'),  # For a specific user
    path('orders/all/', get_all_orders, name='all_orders'),  # For all orders (admin)
     path('orders/status/', get_orders_by_status, name='get_orders_by_status'),  # New endpoint
    path('orders/<int:orderid>/products/', products_in_order, name='products_in_order'),
    path('orders/add/', add_order, name='add_order'), #add order details and orderproduct details
    path('orders/<int:orderid>/', update_order, name='update_order'),
    
    path('categories/', all_categories, name='categories'),
    path('add-categories/', add_category, name='add categories'),
    path('update-categories/', update_category, name='update categories'),
    
    path('accounts/', include('allauth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api-token-auth/', obtain_auth_token),
    
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),# Password reset confirmation (step 2, user submits new password)
    
   #path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),


]

