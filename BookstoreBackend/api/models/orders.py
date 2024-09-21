from django.db import models


class Orders(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True) 
    userid = models.ForeignKey('api.Users', models.DO_NOTHING, db_column='UserID') 
    orderdate = models.DateTimeField(db_column='OrderDate') 
    deliverydate = models.DateTimeField(db_column='DeliveryDate', blank=True, null=True)  
    deliverymethod = models.CharField(db_column='DeliveryMethod', max_length=50)  
    paymentmethod = models.CharField(db_column='PaymentMethod', max_length=50)  
    orderstatus = models.CharField(db_column='OrderStatus', max_length=50)  

    class Meta:
        managed = False
        db_table = 'orders'

class OrderProduct(models.Model):
    orderproductid = models.AutoField(db_column='OrderProductID', primary_key=True)  
    orderid = models.ForeignKey('Orders', models.DO_NOTHING, db_column='OrderID')  
    productid = models.ForeignKey('Products', models.DO_NOTHING, db_column='ProductID')  
    quantity = models.IntegerField(db_column='Quantity') 
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  

    class Meta:
        managed = False
        db_table = 'orderproduct'
