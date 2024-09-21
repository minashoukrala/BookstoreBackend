from django.db import models


class Carts(models.Model):
    cartid = models.IntegerField(db_column='CartID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('api.Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'carts'

class CartProducts(models.Model):
    cartproductid = models.AutoField(db_column='CartProductID', primary_key=True)  # Field name made lowercase.
    cartid = models.ForeignKey('Carts', models.DO_NOTHING, db_column='CartID')  # Field name made lowercase.
    productid = models.ForeignKey('Products', models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cartproducts'
