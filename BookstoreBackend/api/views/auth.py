from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Users
from django.contrib.auth.forms import PasswordResetForm
from ..persmissions import IsNotAuthenticated, IsAdminUser
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse


class RegisterView(APIView):
    # Allow access only to unauthenticated users
    permission_classes = [IsNotAuthenticated]
    def post(self, request):
        # If the user is already authenticated, prevent registration
        if request.user.is_authenticated:
            return Response({'error': 'You are already registered and logged in.'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the data from the request
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        phonenumber = request.data.get('phonenumber')
        gender = request.data.get('gender')
        address = request.data.get('address')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        # Basic validation for missing fields
        if not all([username, password, email, phonenumber, first_name, last_name, gender, address]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username or email already exists
        if Users.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if Users.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new user and hash the password
        user = Users.objects.create_user(
            username=username,
            email=email,
            phonenumber=phonenumber,
            password=password,  # Ensure password is hashed before saving
            first_name=first_name,
            last_name=last_name,
            gender=gender,  # Assuming 'Users' model has a gender field
            address=address  # Assuming 'Users' model has an address field
        )
        user.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    # Allow access only to unauthenticated users
    permission_classes = [IsNotAuthenticated]

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'error': 'You are already logged in.'}, status=status.HTTP_403_FORBIDDEN)

        # Proceed with login
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    # Only authenticated users can log out
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


User = get_user_model()

class CustomPasswordResetForm(PasswordResetForm):
    def save(self, domain_override=None, subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html', use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None, extra_email_context=None):
        
        # Assuming form is already cleaned and validated
        email = self.cleaned_data["email"]
        active_users = User.objects.filter(email__iexact=email, is_active=True)

        for user in active_users:
            # Generate a unique token and UID for the user
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            protocol = 'https' if use_https else 'http'
            domain = "localhost:3000"
            custom_reset_url = f"{protocol}://{domain}/resetpassword/{uid}/{token}/"

            context = {
                'email': user.email,
                'domain': domain,
                'site_name': get_current_site(request).name,
                'uid': uid,
                'user': user,
                'token': token,
                'protocol': protocol,
                'reset_url': custom_reset_url,
            }

            if extra_email_context:
                context.update(extra_email_context)

            email_subject = render_to_string(subject_template_name, context)
            email_subject = ''.join(email_subject.splitlines())  # Email subject *must not* contain newlines
            email_body = render_to_string(email_template_name, context)

            # Send email
            send_mail(email_subject, email_body, from_email, [user.email], html_message=(render_to_string(html_email_template_name, context) if html_email_template_name else None))

# In your view
class CustomPasswordResetView(APIView):
    permission_classes = [IsNotAuthenticated]

    def post(self, request, *args, **kwargs):
        form = CustomPasswordResetForm(data=request.data)
        if form.is_valid():
            form.save(use_https=request.is_secure(), request=request)
            return Response({'message': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        


class CustomPasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            # Decode the user ID from the uidb64 in the URL
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the token is valid for the given user
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and set the new password
        form = SetPasswordForm(user, request.data)
        if form.is_valid():
            form.save()  # This will save the new password
            return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        #Test by {
#    "new_password1": "new_secure_password",
#    "new_password2": "new_secure_password"
#}
