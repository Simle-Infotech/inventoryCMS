from django.db import models


class ShoppingCart(models.Model):
    # order = models.ForeignKey('market.MarketOrder', on_delete=models.CASCADE)
    customer = models.ForeignKey('accounts.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    paid_status = models.IntegerField(choices=(
        (1, "Unpaid"),
        (2, "Paid in Cash"),
        (3, "Paid in Cheque"),
        (4, "Free Distribution")
    ), default=1)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.description != "":
            return self.description
        else:
            return "%s : Cart" % (self.id)
    
    class Meta:
        ordering = ('-paid_status',)


class ShoppingItems(models.Model):
    item = models.ForeignKey('products.ItemColorAvailability', on_delete=models.CASCADE)
    qty = models.IntegerField('Quantity')
    cart = models.ForeignKey('market.ShoppingCart', on_delete=models.CASCADE)
    price = models.FloatField('Rate', default=0)
    taxable = models.BooleanField(default=True)
    tax_included = models.BooleanField(default=False)