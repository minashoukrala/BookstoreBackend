from .user_views import users_list, user_details, is_user_admin, edit_user_info, user_status
from .product_views import all_products_details, product_details, products_by_category, add_product, update_product, delete_product
from .cart_views import user_cart_items, add_item_to_cart, delete_cart_item, modify_cart_item_quantity
from .order_views import products_in_order, add_order, update_order, user_orders_with_products, get_all_orders,get_user_orders, get_orders_by_status
from .auth import LoginView, RegisterView, LogoutView, CustomPasswordResetView, CustomPasswordResetConfirmView
from .catergories import add_category, all_categories, update_category
from . import stripe_views
