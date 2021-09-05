from datetime import time
from django.db import models
from django.utils import timezone
# from datetime import date, datetime


class openingInventory(models.Model):
    product = models.ForeignKey('products.ItemColorAvailability', on_delete=models.CASCADE)
    opening_qty = models.FloatField("Opening Quantity")
    rate = models.FloatField("Opening Rate")
    expiry = models.DateField("Expiry Date")
    entry_date = models.DateField(default=timezone.now)
    entry_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "%s: %.0f on %s" % (self.product, self.opening_qty, self.entry_date)
