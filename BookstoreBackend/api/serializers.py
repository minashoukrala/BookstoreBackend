from rest_framework import serializers
from .models import Admin, Carts, Cartproducts, Orders, Orderproduct, Products, Users
# from django.contrib.auth.models import User

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['adminid', 'userid', 'adminrole']

class CartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = ['cartid', 'userid']

class CartproductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartproducts
        fields = ['cartproductid', 'cartid', 'productid', 'quantity']

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['orderid', 'userid', 'orderdate', 'deliverydate', 'deliverymethod', 'paymentmethod']

class OrderproductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderproduct
        fields = ['orderproductid', 'orderid', 'productid', 'quantity', 'price']

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['productid', 'productname', 'category', 'productdescription', 'productprice', 'productimage', 'availablequantity', 'isrequestable']

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['userid', 'email', 'password', 'firstname', 'lastname', 'address', 'phonenumber', 'username']   