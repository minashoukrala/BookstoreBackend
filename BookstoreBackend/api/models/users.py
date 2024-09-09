from django.db import models

class Users(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=100)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', unique=True, max_length=20)  # Field name made lowercase.
    username = models.CharField(db_column='Username', unique=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'
