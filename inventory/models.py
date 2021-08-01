from datetime import time
from django.db import models
from django.utils import timezone
# from datetime import date, datetime


class opening_inventory(models.Model):
    product = models.ForeignKey('products.Item', on_delete=models.CASCADE)
    opening_qty = models.FloatField("Opening Quantity")
    rate = models.FloatField("Opening Rate")
    expiry = models.DateField("Expiry Date")
    entry_date = models.DateField(default=timezone.now)
    entry_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

