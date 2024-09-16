from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    # AutoField already makes the id incremental and unique by default
    UserID = models.AutoField(primary_key=True)
    email = models.EmailField(db_column='Email', unique=True, max_length=100)
    phonenumber = models.CharField(db_column='PhoneNumber', unique=True, max_length=20)
    address = models.CharField(db_column='Address', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'users'
