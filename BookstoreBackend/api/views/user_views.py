from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import Users, Admin
from ..serializers import UsersSerializer, AdminSerializer
from ..persmissions import IsAdminUser, IsAdminOrOwner

@api_view(['GET'])
@permission_classes([IsAdminUser])# Ensure only authenticated users can access thi
def users_list(request):
    # Fetch all users
    users = Users.objects.all()

    # We assume the UserSerializer is already implemented
    # Serialize user data along with admin status
    user_data = []
    
    for user in users:
        # Serialize user
        user_serializer = UsersSerializer(user)
        
        # Check if the user exists in the Admin table
        is_admin = Admin.objects.filter(userid=user).exists()
        
        # Add admin status to the serialized data
        serialized_user_data = user_serializer.data
        serialized_user_data['is_admin'] = is_admin
        
        # Append the user data with admin status to the final list
        user_data.append(serialized_user_data)
    
    # Return the user details with admin status
    return Response(user_data)


@api_view(['GET'])
@permission_classes([IsAdminOrOwner])
def user_details(request, userid):
    try:
        # Fetch the specific user by ID
        user = Users.objects.get(userid=userid)

        # Serialize user data
        user_serializer = UsersSerializer(user)

        # Check if the user exists in the Admin table
        is_admin = Admin.objects.filter(userid=user).exists()

        # Add the admin status to the serialized data
        user_data = user_serializer.data
        user_data['is_admin'] = is_admin

        # Return the serialized user data with admin status
        return Response(user_data)

    except Users.DoesNotExist:
        # Return a 404 response if the user is not found
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
  
#not sure 
@api_view(['GET'])
@permission_classes([IsAdminUser])
def is_user_admin(request, userid):
    try:
        # Fetch the user by ID
        user = Users.objects.get(userid=userid)

        # Check if the user exists in the Admin table
        is_admin = Admin.objects.filter(userid=user).exists()

        # Return the admin status as JSON
        return Response({'is_admin': is_admin})

    except Users.DoesNotExist:
        # Return a 404 response if the user is not found
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['PATCH'])
@permission_classes([IsAdminOrOwner]) 
def edit_user_info(request, userid):
    """
    Edit user information, including inherited fields from AbstractUser and custom fields.
    Only admins can update the is_staff field.
    """
    try:
        # Fetch the user by ID
        user = Users.objects.get(userid=userid)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Only allow admins to update the is_staff field
    if 'is_staff' in request.data and not request.user.is_staff:
        return Response({'error': 'You do not have permission to edit staff status.'}, status=status.HTTP_403_FORBIDDEN)

    # Allow partial updates of user information
    serializer = UsersSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    #test
    #{
    #"phonenumber": "+123456789",
    #"address": "1234 Main St, Springfield, IL",
    #"first_name": "John",
    #"last_name": "Doe"
    #}