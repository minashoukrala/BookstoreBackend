from django.shortcuts import render
from ..models import Products
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def product_list(request):
    if request.method == 'GET':
        products = Products.objects.all()
        products_data = [{
            'id': product.productid,
            'name': product.productname,
            'price': str(product.productprice),
        } for product in products]
        return JsonResponse(products_data, safe=False)

def product_detail(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Products, pk=product_id)
        return JsonResponse({
            'id': product.productid,
            'name': product.productname,
            'price': str(product.productprice),
            'description': product.productdescription,
            'quantity': product.availablequantity,
        })
