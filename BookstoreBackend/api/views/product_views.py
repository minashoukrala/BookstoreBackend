from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Products, ProductImages, ProductCategory, Category, CartProducts
from ..serializers import ProductsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..persmissions import IsAdminUser, IsNotAuthenticated, IsOwner
from django.db.models import Q
from django.db import IntegrityError
from rest_framework.views import APIView

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
    Return all products that have quantity greater than 0 or are requestable for regular users.
    If the user is an admin, return all products.
    """
    try:
        if request.user.is_staff:  # Check if the user is an admin
            # Admins: Return all products
            products = Products.objects.all()
        else:
            # Regular users: Return only available or requestable products
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

        # Return the serialized product data inside a Response object
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    
    
class ProductListView(APIView):
    permission_classes = [AllowAny]  # Ensure only authenticated users can access

    def get(self, request, category_id=None):
        """
        For regular users:
            - Return products with quantity > 0 or requestable products.
            - Optionally filter by category.
        For admin users:
            - Return all products (with or without category filter).
        """
        if request.user.is_staff:
            # Admin users: Return all products (filter by category if provided)
            if category_id:
                products = Products.objects.filter(productcategory__category__categoryid=category_id)
            else:
                products = Products.objects.all()
        else:
            # Regular users: Only return available or requestable products (filter by category if provided)
            if category_id:
                products = Products.objects.filter(
                    productcategory__category__categoryid=category_id,
                    availablequantity__gt=0
                ) | Products.objects.filter(
                    productcategory__category__categoryid=category_id,
                    isrequestable=True
                )
            else:
                products = Products.objects.filter(availablequantity__gt=0) | Products.objects.filter(isrequestable=True)

        # Serialize the products
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)
    
    
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
@permission_classes([IsAdminUser])  # Only admin users can add products
def add_product(request):
    """
    Adds a new product without categories.
    """
    # Step 1: Deserialize product data
    product_serializer = ProductsSerializer(data=request.data)

    # Step 2: Validate and save the product
    if product_serializer.is_valid():
        product = product_serializer.save()
        return Response({"message": "Product added successfully.", "product_id": product.productid}, status=status.HTTP_201_CREATED)
    else:
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_product_categories(request, productid):
    """
    Associates categories with an existing product using category names.
    """
    try:
        # Fetch the product by its ID
        product = Products.objects.get(pk=productid)
    except Products.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    # Get the category names from the request
    category_names = request.data.get('categories', [])

    if not category_names:
        return Response({"error": "No categories provided."}, status=status.HTTP_400_BAD_REQUEST)

    # Associate categories with the product
    for category_name in category_names:
        try:
            category = Category.objects.get(categoryname=category_name)
            ProductCategory.objects.create(product=product, category=category)
        except Category.DoesNotExist:
            return Response({"error": f"Category '{category_name}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Categories added to the product successfully."}, status=status.HTTP_201_CREATED)



    
    
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
    
    
from django.http import JsonResponse
    
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_related_product_categories(request, productid):
    try:
        # First, delete all related product categories entries
        related_categories = ProductCategory.objects.filter(product_id=productid)
        related_categories_count = related_categories.count()  # Optional: Capture the count for logging or response
        related_categories.delete()

        return JsonResponse({'message': f'Related product categories deleted successfully. Count: {related_categories_count}'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request, productid):
    try:
        # Retrieve the product
        product = Products.objects.get(pk=productid)

        # Attempt to delete all related cart products entries
        cart_product_entries = CartProducts.objects.filter(productid=product)
        cart_product_count = cart_product_entries.count()
        cart_product_entries.delete()

        # Log the action if any cart entries were found and deleted
        if cart_product_count > 0:
            print(f"Deleted {cart_product_count} cart product entries for product {productid}")

        # Delete all related product categories entries
        ProductCategory.objects.filter(product=product).delete()

        # Then, delete the product itself
        product.delete()

        return JsonResponse({'message': 'Product and all related entries deleted successfully'}, status=200)
    except Products.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)