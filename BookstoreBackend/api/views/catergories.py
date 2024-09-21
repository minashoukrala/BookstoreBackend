from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import Category
from ..serializers import CategorySerializer
from ..persmissions import IsAdminUser
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([IsAdminUser])  # Restrict access to admin users
def add_category(request):
    """
    Add a new category with an optional image URL.
    """
    # Step 1: Deserialize the Category data
    category_serializer = CategorySerializer(data=request.data)

    # Step 2: Validate and save the Category if valid
    if category_serializer.is_valid():
        category_serializer.save()  # This will save both categoryname and imageurl
        return Response({'message': 'Category added successfully.'}, status=status.HTTP_201_CREATED)
    
    # Step 3: Return errors if the validation fails
    return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def all_categories(request):
    """
    Fetch and return all categories with their images.
    """
    # Fetch all categories from the database
    categories = Category.objects.all()

    # Serialize the category data
    serializer = CategorySerializer(categories, many=True)

    # Return the serialized category data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_category(request, categoryid):
    """
    Update an existing category by category ID.
    """
    try:
        # Fetch the category by ID
        category = Category.objects.get(categoryid=categoryid)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    # Deserialize and validate the new category data
    serializer = CategorySerializer(category, data=request.data, partial=True)  # partial=True allows partial updates
    if serializer.is_valid():
        serializer.save()  # Save the updated category data
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)