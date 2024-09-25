from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    userid = models.AutoField(db_column='userid', primary_key=True)  # AutoField is implicitly a primary key.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=20, blank=True, null=True)
    address = models.CharField(db_column='address', max_length=255, blank=True, null=True)
    gender = models.CharField(
        db_column='gender', 
        max_length=10, 
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], 
        blank=True, 
        null=True
    )


    class Meta:
        db_table = 'users'
