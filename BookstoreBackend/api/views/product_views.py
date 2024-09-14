from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Products
from ..serializers import ProductsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def all_products_details(request):
    # Fetch all products from the database
    products = Products.objects.all()

    # Serialize the product data
    serializer = ProductsSerializer(products, many=True)

    # Return the serialized product data as a JSON response
    return Response(serializer.data)

@api_view(['GET'])
def product_details(request, productid):
    try:
        # Fetch the specific product by ID
        product = Products.objects.get(productid=productid)

        # Serialize the product data
        serializer = ProductsSerializer(product)

        # Return the serialized product data
        return Response(serializer.data)

    except Products.DoesNotExist:
        # Return a 404 response if the product is not found
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def products_by_category(request, category):
    # Fetch all products that belong to the given category
    try:
        products = Products.objects.filter(category=category)

        # Check if any products exist for the given category
        if not products.exists():
            return Response({'error': 'No products found for this category'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the product data
        serializer = ProductsSerializer(products, many=True)

        # Return the serialized product data
        return Response(serializer.data)
    
    except Exception as e:
        # Catch any other exceptions and return a 500 error with details for debugging
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def product_categories(request):
    try:
        # Query distinct categories from the Products model
        categories = Products.objects.values_list('category', flat=True).distinct()

        # Check if categories exist
        if not categories:
            return Response({'message': 'No categories found'}, status=status.HTTP_404_NOT_FOUND)

        # Return the list of distinct categories
        return Response({'categories': list(categories)}, status=status.HTTP_200_OK)
    
    except Exception as e:
        # Catch any exceptions and return a 500 error with details
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    
@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
def manage_product(request, productid=None):
    # Handle adding a new product (POST)
    if request.method == 'POST':
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle updating an existing product (PUT or PATCH)
    if request.method in ['PUT', 'PATCH']:
        try:
            product = Products.objects.get(productid=productid)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        partial = request.method == 'PATCH'
        serializer = ProductsSerializer(product, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle deleting a product (DELETE)
    if request.method == 'DELETE':
        try:
            product = Products.objects.get(productid=productid)
        except Products.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)