from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .. persmissions import IsNotAuthenticated, IsAdminUser, IsOwner, IsAdminOrOwner
from rest_framework.permissions import IsAuthenticated
from ..models import Carts, CartProducts, Products
from ..serializers import CartProductsSerializer # Assuming this is your serializer for cart products

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this
def user_cart_items(request):
    try:
        # Fetch the cart for the current authenticated user
        cart = Carts.objects.get(userid=request.user.userid)

        # Fetch all items in the user's cart
        cart_items = CartProducts.objects.filter(cartid=cart.cartid)

        # Serialize the cart items with product details
        serializer = CartProductsSerializer(cart_items, many=True)

        # Return the serialized cart items
        return Response(serializer.data)

    except Carts.DoesNotExist:
        # Return a 404 response if the user does not have a cart
        return Response({'error': 'Cart not found for this user'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access this
def add_item_to_cart(request):
    """
    Add an item to the user's cart.
    The request must contain the user ID, product ID, and quantity.
    """
    try:
        # Get the user ID and product details from the request
        userid = request.user.userid
        productid = request.data.get('productid')
        quantity = request.data.get('quantity')

        # Ensure the product exists
        try:
            product = Products.objects.get(productid=productid)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user already has a cart; if not, create one
        cart, created = Carts.objects.get_or_create(userid=userid)

        # Check if the product is already in the cart
        cart_product, created = CartProducts.objects.get_or_create(
            cartid=cart,
            productid=product,
            defaults={'quantity': quantity}
        )

        # If the product is already in the cart, update the quantity
        if not created:
            cart_product.quantity += int(quantity)
            cart_product.save()

        return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #test case{
    #"productid": 1,
    #"quantity": 2
    #}
    
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def modify_cart_item_quantity(request):
    """
    Modify the quantity of a product in the user's cart.
    The request must contain the product ID and the new quantity.
    """
    try:
        # Get the user ID from the request (authenticated user)
        userid = request.user.userid
        
        # Get the product ID and new quantity from the request data
        productid = request.data.get('productid')
        new_quantity = request.data.get('quantity')

        # Check if both productid and new_quantity are provided
        if not productid or not new_quantity:
            return Response({'error': 'Product ID and quantity are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user has a cart
        try:
            cart = Carts.objects.get(userid=userid)
        except Carts.DoesNotExist:
            return Response({'error': 'Cart not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the product is already in the user's cart
        try:
            cart_product = CartProducts.objects.get(cartid=cart.cartid, productid=productid)
        except CartProducts.DoesNotExist:
            return Response({'error': 'Product not found in the cart.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the product quantity
        cart_product.quantity = new_quantity
        cart_product.save()

        # Serialize and return the updated cart item
        serializer = CartProductsSerializer(cart_product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

     #test case{
    #"productid": 1,
    #"quantity": 2
    #}
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # Ensure that only authenticated users can delete items
def delete_cart_item(request):
    """
    Delete a specific product from the user's cart based on the product ID sent in the request body.
    """
    try:
        # Get the current authenticated user's ID
        userid = request.user.userid  # Assuming the `id` is the correct user identifier

        # Get the product ID from the request body
        productid = request.data.get('productid')

        # Check if the product ID was provided
        if not productid:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user has a cart
        try:
            cart = Carts.objects.get(userid=userid)
        except Carts.DoesNotExist:
            return Response({'error': 'Cart not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the product exists in the user's cart
        try:
            cart_product = CartProducts.objects.get(cartid=cart.cartid, productid=productid)
        except CartProducts.DoesNotExist:
            return Response({'error': 'Product not found in the cart.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the product from the cart
        cart_product.delete()

        return Response({'message': 'Product removed from cart successfully.'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


