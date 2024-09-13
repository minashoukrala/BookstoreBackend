from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Carts, Cartproducts, Products
from ..serializers import CartproductsSerializer # Assuming this is your serializer for cart products

@api_view(['GET'])
def user_cart_items(request, userid):
    try:
        # Fetch the cart for the specific user
        cart = Carts.objects.get(userid=userid)

        # Fetch all items in the user's cart
        cart_items = Cartproducts.objects.filter(cartid=cart.cartid)

        # Serialize the cart items
        serializer = CartproductsSerializer(cart_items, many=True)

        # Return the serialized cart items
        return Response(serializer.data)

    except Carts.DoesNotExist:
        # Return a 404 response if the user does not have a cart
        return Response({'error': 'Cart not found for this user'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'DELETE'])
def modify_cart_item(request, userid, productid=None):
    try:
        # Get the cart for the specific user
        cart = Carts.objects.get(userid=userid)
    except Carts.DoesNotExist:
        return Response({'error': 'Cart not found for this user'}, status=status.HTTP_404_NOT_FOUND)

    # Handle adding a new item to the cart (POST)
    if request.method == 'POST':
        try:
            product = Products.objects.get(productid=productid)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the product already exists in the cart
        cart_item, created = Cartproducts.objects.get_or_create(cartid=cart, productid=product)
        if not created:
            # If it exists, update the quantity
            cart_item.quantity += request.data.get('quantity', 1)  # Default is adding 1 if not specified
        else:
            cart_item.quantity = request.data.get('quantity', 1)

        cart_item.save()
        serializer = CartproductsSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Handle removing an item from the cart (DELETE)
    elif request.method == 'DELETE':
        try:
            cart_item = Cartproducts.objects.get(cartid=cart, productid=productid)
        except Cartproducts.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)