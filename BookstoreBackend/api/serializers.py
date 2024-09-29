from rest_framework import serializers
from .models import Users, Products, ProductImages, ProductCategory, Orders, OrderProduct, Category, Carts, CartProducts, Admin
from django.db import models

# Serializer for the Users model
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['userid', 'username', 'email', 'first_name', 'last_name', 'phonenumber', 'address', 'is_staff', 'date_joined']  # Include custom fields

# Serializer for the Products model
class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['productid', 'productname', 'productdescription', 'productprice', 'availablequantity', 'isrequestable']

# Serializer for ProductImages
class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['imageid', 'product', 'imageurl']

# Serializer for ProductCategory
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['product', 'category']

# Serializer for the Orders model
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['orderid', 'userid', 'orderdate', 'totalprice', 'orderstatus']

# Serializer for the OrderProduct model
class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['orderid', 'productid', 'quantity', 'price']


# Serializer for the Categories model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['categoryid', 'categoryname', 'imageurl']


# Serializer for the Carts model
class CartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = ['cartid', 'userid']

# Serializer for CartProducts
class CartProductsSerializer(serializers.ModelSerializer):
    productid = ProductsSerializer()  # Nest ProductSerializer to include product details
    class Meta:
        model = CartProducts
        fields = ['cartproductid', 'cartid', 'productid', 'quantity']

# Serializer for the Admin model
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['adminid', 'userid', 'adminrole']
        

class OrderSerializer(serializers.ModelSerializer):
    # Nested serializer to show order products
    order_items = serializers.SerializerMethodField()
    customer = serializers.CharField(source='userid.username', read_only=True)  # Assuming Users model has username field
    total_price = serializers.SerializerMethodField()  # Field for total price
    items_count = serializers.SerializerMethodField()  # Field for number of items

    class Meta:
        model = Orders
        fields = ['orderid', 'orderdate', 'customer', 'orderstatus', 'order_items', 'total_price','items_count']

    def get_order_items(self, obj):
        # Get all products associated with the order
        order_products = OrderProduct.objects.filter(orderid=obj.orderid)
        return OrderProductSerializer(order_products, many=True).data

    def get_total_price(self, obj):
        # Manually sum the prices of all products associated with the order
        order_products = OrderProduct.objects.filter(orderid=obj.orderid)
        total = sum([item.price * item.quantity for item in order_products])
        return total if total else 0.00
    
    def get_items_count(self, obj):
        # Count the total number of items (sum of quantities) in the order
        order_products = OrderProduct.objects.filter(orderid=obj.orderid)
        total_items = sum([item.quantity for item in order_products])
        return total_items if total_items else 0

        
