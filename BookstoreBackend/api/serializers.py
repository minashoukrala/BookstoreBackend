from rest_framework import serializers
from .models import Users, Products, ProductImages, ProductCategory, Orders, OrderProduct, Category, Carts, CartProducts, Admin

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
        fields = ['orderid', 'userid', 'orderdate', 'totalprice', 'status']

# Serializer for the OrderProduct model
class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['orderproductid', 'orderid', 'productid', 'quantity', 'price']


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
    class Meta:
        model = CartProducts
        fields = ['cartproductid', 'cartid', 'productid', 'quantity']

# Serializer for the Admin model
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['adminid', 'userid', 'adminrole']
        
