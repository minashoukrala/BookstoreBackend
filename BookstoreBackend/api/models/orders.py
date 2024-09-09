from django.db import models


class Orders(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('api.Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    orderdate = models.DateTimeField(db_column='OrderDate')  # Field name made lowercase.
    deliverydate = models.DateTimeField(db_column='DeliveryDate', blank=True, null=True)  # Field name made lowercase.
    deliverymethod = models.CharField(db_column='DeliveryMethod', max_length=50)  # Field name made lowercase.
    paymentmethod = models.CharField(db_column='PaymentMethod', max_length=50)  # Field name made lowercase.
    orderstatus = models.CharField(db_column='OrderStatus', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orders'

class Orderproduct(models.Model):
    orderproductid = models.AutoField(db_column='OrderProductID', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey('Orders', models.DO_NOTHING, db_column='OrderID')  # Field name made lowercase.
    productid = models.ForeignKey('Products', models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orderproduct'
