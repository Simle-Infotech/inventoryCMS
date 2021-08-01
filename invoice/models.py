from products.models import Item
from django.db import models

class InvoiceMeta(models.Model):
    total = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    paid_amount = models.FloatField(null=True, blank=True, default=0)
    date = models.DateField(null=True, blank=True)
    to_pay = models.FloatField(null=True, blank=True, default=0)
    discount = models.FloatField(null=True, blank=True, default=0)
    notes = models.TextField(blank=True, null=True)
    bill_no = models.CharField(verbose_name="Bill No", null=True, blank=True, max_length=500)
    is_vat = models.BooleanField(default=False)

    class Meta:
        abstract = True


class salesInvoice(InvoiceMeta):
    issued_for = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)
    issued_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    is_posted = models.BooleanField(default=False)

    def __str__(self):
        try:
            return self.issued_for.name + " " + self.issued_by.name
        except:
            try:
                return self.issued_for.name
            except:
                return self.total


class purchaseInvoice(InvoiceMeta):
    issued_by = models.ForeignKey('accounts.Dealer', on_delete=models.CASCADE)
    posted_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    pass


class ItemsMeta(models.Model):
    product = models.ForeignKey('products.Item', on_delete=models.CASCADE)
    quantity = models.FloatField()
    rate = models.FloatField()
    taxable = models.BooleanField(default=False)
    taxInc = models.BooleanField("Included Tax", default = True)
    expiryDate = models.DateField("Expiry Date")

    class Meta:
        abstract = True


class salesItem(ItemsMeta):
    salesInvoice = models.ForeignKey('invoice.salesInvoice', on_delete=models.CASCADE)


class purchaseItem(ItemsMeta):
    purchaseInvoice = models.ForeignKey('invoice.purchaseInvoice', on_delete=models.CASCADE)
