from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Orders

def order_list(request, user_id):
    if request.method == 'GET':
        orders = Orders.objects.filter(user_id=user_id)
        orders_data = [{
            'id': order.id,
            'order_date': order.order_date,
            'status': order.order_status
        } for order in orders]
        return JsonResponse(orders_data, safe=False)

def order_detail(request, order_id):
    if request.method == 'GET':
        order = get_object_or_404(Orders, pk=order_id)
        order_products = order.orderproduct_set.all()  # Assuming a reverse relation exists
        products_data = [{
            'product_name': order_product.product.product_name,
            'quantity': order_product.quantity,
            'price': str(order_product.price)
        } for order_product in order_products]
        return JsonResponse({
            'order_id': order.id,
            'order_date': order.order_date,
            'delivery_method': order.delivery_method,
            'payment_method': order.payment_method,
            'products': products_data
        })
