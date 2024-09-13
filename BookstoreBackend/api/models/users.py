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

# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

# class UsersManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)  # Hash the password using Django's method
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(username, email, password, **extra_fields)


# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# class Users(AbstractBaseUser, PermissionsMixin):
#     userid = models.AutoField(primary_key=True)
#     email = models.EmailField(unique=True)
#     username = models.CharField(unique=True, max_length=45)
#     firstname = models.CharField(max_length=50)
#     lastname = models.CharField(max_length=50)
#     address = models.CharField(max_length=255)
#     phonenumber = models.CharField(unique=True, max_length=20)
    
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     # Adding related_name to avoid clashes with auth.User
#     groups = models.ManyToManyField(Group, related_name='custom_user_groups')
#     user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

#     objects = UsersManager()

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     class Meta:
#         managed = False  # Assuming you're working with an existing database
#         db_table = 'users'
