from django.db import models
from ..models import Users  # Make sure to import Users correctly

class Admin(models.Model):
    adminid = models.AutoField(db_column='AdminID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(Users, models.DO_NOTHING, db_column='UserID')  # Reference to Users model
    adminrole = models.CharField(db_column='AdminRole', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin'
