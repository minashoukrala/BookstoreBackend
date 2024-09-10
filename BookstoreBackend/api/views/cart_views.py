from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Carts

def view_cart(request, user_id):
    if request.method == 'GET':
        cart = get_object_or_404(Carts, user_id=user_id)
        cart_products = cart.cartproduct_set.all()  # Assuming a reverse relation exists
        products_data = [{
            'product_name': cart_product.product.product_name,
            'quantity': cart_product.quantity
        } for cart_product in cart_products]
        return JsonResponse({'cart_id': cart.cartid, 'products': products_data})
