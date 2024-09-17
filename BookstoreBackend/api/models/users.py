from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    userid = models.AutoField(primary_key=True, db_column='UserId')  # Ensure case sensitivity matches
    email = models.EmailField(unique=True, max_length=100, db_column='Email')
    password = models.CharField(max_length=255, db_column='Password')  # If you're manually handling passwords (usually not recommended)
    phonenumber = models.CharField(max_length=20, unique=True, db_column='PhoneNumber')
    address = models.CharField(max_length=255, null=True, blank=True, db_column='Address')
    first_name = models.CharField(max_length=150, db_column='first_name')  # Added based on your DB screenshot
    last_name = models.CharField(max_length=150, db_column='last_name')  # Added based on your DB screenshot

    class Meta:
        db_table = 'users'
