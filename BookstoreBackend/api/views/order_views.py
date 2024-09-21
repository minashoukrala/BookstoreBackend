from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import status 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import Orders, OrderProduct
from ..serializers import OrdersSerializer, OrderProductSerializer  # Assuming this serializer is implemented for Orders
from ..persmissions import IsAdminUser, IsOwner, IsAdminOrOwner
from django.utils import timezone
from datetime import timedelta

@api_view(['GET'])
@permission_classes([IsAdminOrOwner])
def user_orders_with_products(request, userid):
    """
    Return all orders for a specific user, along with the products in each order, sorted by newest to oldest.
    """
    # Fetch all orders for the specified user, sorted by order date (newest to oldest)
    orders = Orders.objects.filter(userid=userid).order_by('-orderdate')

    # Check if the user has any orders
    if not orders.exists():
        return Response({'message': 'No orders found for this user.'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the orders, including related products
    serializer = OrdersSerializer(orders, many=True)

    # Return the serialized order data
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def products_in_order(request, orderid):
    try:
        # Fetch the specific order by ID
        order = Orders.objects.get(orderid=orderid)

        # Fetch all products associated with this order
        order_products = OrderProduct.objects.filter(orderid=orderid)

        # Check if any products exist for this order
        if not order_products.exists():
            return Response({'error': 'No products found for this order'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the order products data
        serializer = OrderProductSerializer(order_products, many=True)

        # Return the serialized products in the order
        return Response(serializer.data)

    except Orders.DoesNotExist:
        # Return a 404 response if the order does not exist
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def orders_not_delivered(request):
    # Filter all orders where orderstatus is not 'delivered', and sort by newest to oldest
    orders = Orders.objects.exclude(orderstatus='delivered').order_by('-orderdate')

    # Check if there are any orders that match the criteria
    if not orders.exists():
        return Response({'message': 'No orders with status other than delivered'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the orders
    serializer = OrdersSerializer(orders, many=True)

    # Return the serialized data
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def delivered_orders(request):
    # Filter all orders where orderstatus is 'delivered', and sort by newest to oldest
    orders = Orders.objects.filter(orderstatus='delivered').order_by('-orderdate')

    # Check if there are any delivered orders
    if not orders.exists():
        return Response({'message': 'No delivered orders found'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the orders
    serializer = OrdersSerializer(orders, many=True)

    # Return the serialized data
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order(request):
    # Handle adding a new order
    serializer = OrdersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_order(request, orderid):
    try:
        # Fetch the order by ID
        order = Orders.objects.get(orderid=orderid)
    except Orders.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    # Use PATCH for partial updates or PUT for full updates
    partial = request.method == 'PATCH'
    serializer = OrdersSerializer(order, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminOrOwner])  # Assuming you have this permission in place
def delete_order(request, orderid):
    """
    Delete an order only if the user is the owner or an admin, and it can only be deleted within the first 24 hours by the owner.
    """
    try:
        # Fetch the specific order by ID
        order = Orders.objects.get(orderid=orderid)

        # Check if the current user is the order owner
        if request.user != order.userid and not request.user.is_staff:
            return Response({'error': 'You do not have permission to delete this order.'}, status=status.HTTP_403_FORBIDDEN)

        # Calculate the time difference between now and the order date
        time_difference = timezone.now() - order.orderdate

        # Allow deletion by the owner only if within 24 hours
        if request.user == order.userid and time_difference > timedelta(hours=24):
            return Response({'error': 'You can only delete the order within 24 hours after it was placed.'}, status=status.HTTP_403_FORBIDDEN)

        # If conditions are satisfied, delete the order
        order.delete()
        return Response({'message': 'Order deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    except Orders.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)