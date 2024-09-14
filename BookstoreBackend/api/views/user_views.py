from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import Users, Admin
from ..serializers import UsersSerializer, AdminSerializer

@api_view(['GET'])
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
    
    
#only accessed by admin    
@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
def manage_user(request, userid=None):
    # Handle adding a new user (POST)
    if request.method == 'POST':
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle updating an existing user (PUT or PATCH)
    if request.method in ['PUT', 'PATCH']:
        try:
            user = Users.objects.get(userid=userid)
        except Users.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        partial = request.method == 'PATCH'
        serializer = UsersSerializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle deleting a user (DELETE)
    if request.method == 'DELETE':
        try:
            user = Users.objects.get(userid=userid)
        except Users.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

#only accessed by admin
@api_view(['POST', 'PUT', 'PATCH', 'DELETE'])
def manage_admin(request, adminid=None):
    # Handle adding a new admin (POST)
    if request.method == 'POST':
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle updating an existing admin (PUT or PATCH)
    if request.method in ['PUT', 'PATCH']:
        try:
            admin = Admin.objects.get(adminid=adminid)
        except Admin.DoesNotExist:
            return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        partial = request.method == 'PATCH'  # Partial update for PATCH
        serializer = AdminSerializer(admin, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle removing an admin (DELETE)
    if request.method == 'DELETE':
        try:
            admin = Admin.objects.get(adminid=adminid)
        except Admin.DoesNotExist:
            return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

        admin.delete()
        return Response({'message': 'Admin removed successfully'}, status=status.HTTP_204_NO_CONTENT)
    

#only accessed by the users session
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_user(request, userid):
    try:
        # Get the user by ID
        user = Users.objects.get(userid=userid)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Handle partial or full update
    partial = request.method == 'PATCH'
    serializer = UsersSerializer(user, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)