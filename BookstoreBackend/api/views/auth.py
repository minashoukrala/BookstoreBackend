from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..models import Users

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        print(username)
        password = request.data.get('password')
        email = request.data.get('email')
        phonenumber = request.data.get('phonenumber')
        
        # Create new user
        user = Users.objects.create_user(
            username=username,
            email=email,
            phonenumber=phonenumber,
            password=password
        )
        user.save()
        
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
