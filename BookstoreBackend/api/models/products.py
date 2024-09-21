from django.db import models
from .categories import Category

class Products(models.Model):
    productid = models.AutoField(db_column='ProductID', primary_key=True) 
    productname = models.CharField(db_column='ProductName', max_length=100) 
    productdescription = models.TextField(db_column='ProductDescription') 
    productprice = models.DecimalField(db_column='ProductPrice', max_digits=10, decimal_places=2)  
    availablequantity = models.IntegerField(db_column='AvailableQuantity')
    isrequestable = models.BooleanField(db_column='IsRequestable') 
    class Meta:
        managed = False
        db_table = 'products'

   
        
class ProductImages(models.Model):
    imageid = models.AutoField(db_column='ImageID', primary_key=True)  # Field name made lowercase.
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING, db_column='ProductID')  # Foreign key to Products table.
    imageurl = models.CharField(db_column='ImageURL', max_length=255)  # URL or path to the product image.

    class Meta:
        managed = False
        db_table = 'product_images'

        

class ProductCategory(models.Model):
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING, db_column='ProductID')  # Foreign key to Products
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_column='CategoryID')  # Foreign key to Categories

    class Meta:
        managed = False
        db_table = 'product_category'
        
    