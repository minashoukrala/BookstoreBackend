from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from rest_framework import status 
from ..models import Orders, Orderproduct
from ..serializers import OrdersSerializer, OrderproductSerializer  # Assuming this serializer is implemented for Orders

@api_view(['GET'])
def user_orders(request, userid):
    try:
        # Fetch all orders for the specific user
        orders = Orders.objects.filter(userid=userid)

        # Check if any orders exist for the user
        if not orders.exists():
            return Response({'error': 'No orders found for this user'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the order data
        serializer = OrdersSerializer(orders, many=True)

        # Return the serialized order data
        return Response(serializer.data)

    except Orders.DoesNotExist:
        # Return a 404 response if no orders are found
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def products_in_order(request, orderid):
    try:
        # Fetch the specific order by ID
        order = Orders.objects.get(orderid=orderid)

        # Fetch all products associated with this order
        order_products = Orderproduct.objects.filter(orderid=orderid)

        # Check if any products exist for this order
        if not order_products.exists():
            return Response({'error': 'No products found for this order'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the order products data
        serializer = OrderproductSerializer(order_products, many=True)

        # Return the serialized products in the order
        return Response(serializer.data)

    except Orders.DoesNotExist:
        # Return a 404 response if the order does not exist
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
def orders_not_delivered(request):
    # Filter all orders where orderstatus is not 'delivered'
    orders = Orders.objects.exclude(orderstatus='delivered')

    # Check if there are any orders that match the criteria
    if not orders.exists():
        return Response({'message': 'No orders with status other than delivered'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the orders
    serializer = OrdersSerializer(orders, many=True)

    # Return the serialized data
    return Response(serializer.data)

@api_view(['GET'])
def delivered_orders(request):
    # Filter all orders where orderstatus is 'delivered'
    orders = Orders.objects.filter(orderstatus='delivered')

    # Check if there are any delivered orders
    if not orders.exists():
        return Response({'message': 'No delivered orders found'}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the orders
    serializer = OrdersSerializer(orders, many=True)

    # Return the serialized data
    return Response(serializer.data)


@api_view(['POST'])
def add_order(request):
    # Handle adding a new order
    serializer = OrdersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'PATCH'])
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