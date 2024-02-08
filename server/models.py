from django.db import models

# Create your models here.
class StockModel(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    trade_code = models.CharField(max_length=20)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()