
from django.db import models


class Category(models.Model):
    categoryid = models.AutoField(db_column='CategoryID', primary_key=True)  
    categoryname = models.CharField(db_column='CategoryName', max_length=50)
    imageurl = models.CharField(db_column='ImageURL', max_length=255)  # URL or path to the category image.

    class Meta:
        managed = False
        db_table = 'categories'
        