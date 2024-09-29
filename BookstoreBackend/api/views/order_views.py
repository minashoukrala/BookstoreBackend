from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import status 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import Orders, OrderProduct
from ..serializers import OrdersSerializer, OrderProductSerializer, OrderSerializer  # Assuming this serializer is implemented for Orders
from ..persmissions import IsAdminUser, IsOwner, IsAdminOrOwner
from django.utils import timezone
from datetime import timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
    serializer = OrderSerializer(order, data=request.data, partial=partial)

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
    
    
    # View to get orders for a specific user
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def get_user_orders(request):
    user = request.user  # Get the authenticated user
    orders = Orders.objects.filter(userid=user.userid)  # Filter orders by the user's ID
    serializer = OrderSerializer(orders, many=True)  # Serialize the orders
    return Response(serializer.data)


# View to get all orders (admin only)
@api_view(['GET'])
@permission_classes([IsAdminUser])  # Ensure only authenticated users can access this
def get_all_orders(request):
    if not request.user.is_staff:  # Ensure only admins can access all orders
        return Response({'error': 'Unauthorized access'}, status=403)

    orders = Orders.objects.all()  # Get all orders
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# View to get all orders by status (authenticated users only)
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def get_orders_by_status(request):
    status = request.query_params.get('status')  # Get the status from query params
    if not status:
        return Response({'error': 'Status parameter is required'}, status=400)

    # Filter orders based on the status
    if request.user.is_staff:
        # Admins can see all orders
        orders = Orders.objects.filter(status=status)
    else:
        # Regular users can only see their own orders
        orders = Orders.objects.filter(userid=request.user.userid, status=status)

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)