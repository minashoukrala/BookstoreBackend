from django.db import models

class Products(models.Model):
    productid = models.AutoField(db_column='ProductID', primary_key=True)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=100)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50)  # Field name made lowercase.
    productdescription = models.TextField(db_column='ProductDescription')  # Field name made lowercase. This field type is a guess.
    productprice = models.DecimalField(db_column='ProductPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    productimage = models.CharField(db_column='ProductImage', max_length=255)  # Field name made lowercase.
    availablequantity = models.IntegerField(db_column='AvailableQuantity')  # Field name made lowercase.
    isrequestable = models.BooleanField(db_column='IsRequestable')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'products'
