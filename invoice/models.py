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
    order_no = models.ForeignKey('market.ShoppingCart', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        try:
            return self.issued_for.name + " " + self.issued_by.name
        except:
            try:
                return self.issued_for.name
            except:
                return self.total
    
    def save(self, *args, **kwargs):
        if self.vat_bill_no != None:
            self.is_vat = True
        super(salesInvoice, self).save(*args, **kwargs)


class purchaseInvoice(InvoiceMeta):
    issued_by = models.ForeignKey('accounts.Dealer', on_delete=models.CASCADE)
    posted_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    pass


class ItemsMeta(models.Model):
    product = models.ForeignKey('products.ItemColorAvailability', on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField('Description', max_length=300, null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    qty = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    taxable = models.BooleanField(default=False)
    tax_include = models.BooleanField("Included Tax", default = True)
    expiryDate = models.DateField("Expiry Date", null=True, blank=True)
    entry_date = models.DateField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class salesItem(ItemsMeta):
    salesInvoice = models.ForeignKey('invoice.salesInvoice', on_delete=models.CASCADE)



class purchaseItem(ItemsMeta):
    purchaseInvoice = models.ForeignKey('invoice.purchaseInvoice', on_delete=models.CASCADE)
