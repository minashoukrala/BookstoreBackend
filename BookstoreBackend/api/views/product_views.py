from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Products, ProductImages, ProductCategory 
from ..serializers import ProductsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..persmissions import IsAdminUser, IsNotAuthenticated, IsOwner
from django.db.models import Q
from django.db import IntegrityError

@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_products_details(request):
    # Fetch all products from the database
    products = Products.objects.all()

    # Serialize the product data
    serializer = ProductsSerializer(products, many=True)

    # Return the serialized product data as a JSON response
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def available_or_requestable_products(request):
    """
    Return all products that have quantity greater than 0 or are requestable.
    """
    try:
        # Filter products where availablequantity > 0 or isrequestable is True
        products = Products.objects.filter(availablequantity__gt=0) | Products.objects.filter(isrequestable=True)

        # Serialize the products
        serializer = ProductsSerializer(products, many=True)

        # Return the serialized product data
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
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
@permission_classes([IsAdminUser])
def products_by_category(request, categoryid):
    try:
        # Step 1: Get all products for the specified category ID
        product_categories = ProductCategory.objects.filter(category_id=categoryid)

        # Step 2: Extract the product IDs from the product categories
        product_ids = product_categories.values_list('product_id', flat=True)

        # Step 3: Get all products that belong to the category
        products = Products.objects.filter(productid__in=product_ids)

        # Step 4: Serialize the product data
        serializer = ProductsSerializer(products, many=True)

        # Step 5: Return the serialized product data
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ProductCategory.DoesNotExist:
        return Response({'error': 'Category not found or no products available for this category.'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['GET'])
@permission_classes([AllowAny])
def products_by_category_with_quantity_or_requestable(request, categoryid):
    try:
        # Step 1: Get all products for the specified category ID
        product_categories = ProductCategory.objects.filter(category_id=categoryid)

        # Step 2: Extract the product IDs from the product categories
        product_ids = product_categories.values_list('product_id', flat=True)

        # Step 3: Filter products that belong to the category and have quantity > 0 or are requestable
        products = Products.objects.filter(productid__in=product_ids).filter(
            availablequantity__gt=0) | Products.objects.filter(isrequestable=True, productid__in=product_ids)

        # Step 4: Serialize the filtered product data
        serializer = ProductsSerializer(products, many=True)

        # Step 5: Return the serialized product data
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ProductCategory.DoesNotExist:
        return Response({'error': 'Category not found or no products available for this category.'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def search_products_by_user_input(request):
    """
    Search for products based on user input for text and optionally by category name.
    """
    # Get the search text and category name from the request data
    search_text = request.data.get('text', '').strip()
    category_name = request.data.get('category', None)

    # Step 1: Filter products by the search text in the product name (case insensitive)
    products = Products.objects.filter(name__icontains=search_text)

    # Step 2: If a category name is provided, filter by category name
    if category_name:
        # Step 2a: Fetch the product categories by the given category name
        product_categories = ProductCategory.objects.filter(category_name__iexact=category_name)
        
        # Step 2b: Extract the product IDs from the filtered categories
        product_ids = product_categories.values_list('product_id', flat=True)

        # Step 2c: Filter products that belong to the category with the given name
        products = products.filter(productid__in=product_ids)

    # Step 3: Serialize the product data
    serializer = ProductsSerializer(products, many=True)

    # Step 4: Return the serialized product data
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAdminUser])  # Only authenticated users can add products
def add_product(request):
    """
    Add a new product to the database.
    """
    # Deserialize the product data from the request
    serializer = ProductsSerializer(data=request.data)

    # Check if the data is valid
    if serializer.is_valid():
        try:
            # Save the product data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "Product with this ID or name already exists."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_product(request, productid):
    """
    Update an existing product by product ID.
    """
    try:
        # Fetch the specific product by product ID
        product = Products.objects.get(productid=productid)
    except Products.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    # Deserialize and validate the new product data
    serializer = ProductsSerializer(product, data=request.data, partial=True)  # Use partial=True to allow partial updates
    if serializer.is_valid():
        serializer.save()  # Save the updated product data
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request, productid):
    """
    Delete a product by product ID.
    """
    try:
        # Fetch the specific product by product ID
        product = Products.objects.get(productid=productid)
    except Products.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    # Delete the product
    product.delete()
    return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)