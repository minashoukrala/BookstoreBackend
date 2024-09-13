from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password  # Correctly import these

from ..models.users import Users
from rest_framework.authtoken.models import Token
from ..serializers import UsersSerializer

@csrf_exempt
@api_view(['POST'])
def signup(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(commit=False)
        user.password = make_password(request.data['password'])  # Hash the password manually
        user.save()
        
        # Create token for the new user
        token = Token.objects.create(user=user)
        
        # Return the updated user data (after save)
        updated_serializer = UsersSerializer(user)
        return Response({'token': token.key, 'user': updated_serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def login(request):
    try:
        user = Users.objects.get(username=request.data['username'])
    except Users.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    # Check the password
    if not check_password(request.data['password'], user.password):  # Manually check the password
        return Response("Incorrect password", status=status.HTTP_401_UNAUTHORIZED)

    # Delete any existing tokens for the user (optional, in case you want to invalidate old tokens)
    Token.objects.filter(user=user).delete()

    # Authentication successful: create a new token
    token = Token.objects.create(user=user)
    
    # Return the user data and token
    serializer = UsersSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("Token is valid. Passed authentication.")

# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.authentication import SessionAuthentication, TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status

# from django.shortcuts import get_object_or_404
# from django.contrib.auth.hashers import make_password  # To hash the password
# from rest_framework.authtoken.models import Token

# from ..models import Users  # Import your custom Users model
# from ..serializers import UsersSerializer

# @api_view(['POST'])
# def signup(request):
#     serializer = UsersSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save(commit=False)  # Save the user without committing to the database
#         user.password = make_password(request.data['password'])  # Manually hash the password
#         user.save()
#         token = Token.objects.create(user=user)
#         return Response({'token': token.key, 'user': serializer.data})
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Changed status to 400 for bad request

# @api_view(['POST'])
# def login(request):
#     user = get_object_or_404(Users, username=request.data['username'])  # Use your custom Users model
#     if not user.check_password(request.data['password']):  # Check if the password is correct
#         return Response("Incorrect password", status=status.HTTP_401_UNAUTHORIZED)  # Return 401 for unauthorized
#     token, created = Token.objects.get_or_create(user=user)
#     serializer = UsersSerializer(user)
#     return Response({'token': token.key, 'user': serializer.data})

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     return Response("passed!")
