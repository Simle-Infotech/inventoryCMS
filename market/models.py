from django.db.models import Sum, Q, F, Value
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class ShoppingCart(models.Model):
    # order = models.ForeignKey('market.MarketOrder', on_delete=models.CASCADE)
    customer = models.ForeignKey('accounts.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    paid_status = models.IntegerField(choices=(
        (1, "Unpaid"),
        (2, "Paid in Cash"),
        (3, "Paid in Cheque"),
        (4, "Free Distribution"),
        (5, "Marked for Delivery")
    ), default=1)
    description = models.TextField(blank=True, null=True)
    total = models.FloatField(default=0.0)
    total_tax = models.FloatField(default=0.0)
    cart_created = models.DateTimeField(auto_now_add=True )

    def __str__(self):
        if self.description != "":
            return self.description
        else:
            return "%s : Cart" % (self.id)
    
    def save(self, *args, **kwargs):
        self.total = self.get_total
        self.total_tax = self.get_total_tax
        super(ShoppingCart, self).save(*args, **kwargs)
    
    @property
    def get_total(self):
        items = self.shoppingitems_set.all()
        mytotal = 0
        # Tax Included and Tax Excluded Items (Rate * Quantity)
        tax_inc_items = items.filter(Q(Q(taxable = True) & Q(tax_included = True)) | Q(taxable=False))
        if tax_inc_items.count()>0:
            mytotal += tax_inc_items.aggregate(
                total = Sum(F('price') * F('qty'))
            )['total']
        tax = items.filter(taxable=True)
        if tax.count()>0:
            mytotal += tax.aggregate(
                total = Sum(F('price') * F('qty') * Value(settings.TOTAL_WITH_TAX))
            )['total']
        
        return mytotal
    
    @property
    def get_total_tax(self):
        items = self.shoppingitems_set.all()
        mytotal = 0
        # Tax Included Items
        tax_inc_items = items.filter(Q(Q(taxable = True) & Q(tax_included = True)))
        if tax_inc_items.count()>0:
            mytotal += tax_inc_items.aggregate(
                total = Sum(F('price') * F('qty'))
            )['total'] / settings.TOTAL_WITH_TAX * settings.TAX

        tax = items.filter(taxable=True) 
        if tax.count()>0:
            mytotal += tax.aggregate(
                total = Sum(F('price') * F('qty'))
            )['total'] * settings.TAX
        
        return mytotal

    class Meta:
        ordering = ('-paid_status',)


class ShoppingItems(models.Model):
    item = models.ForeignKey('products.ItemColorAvailability', on_delete=models.CASCADE)
    qty = models.IntegerField('Quantity')
    cart = models.ForeignKey('market.ShoppingCart', on_delete=models.CASCADE)
    price = models.FloatField('Rate', default=0)
    taxable = models.BooleanField(default=True)
    tax_included = models.BooleanField(default=False)

    class Meta:
        unique_together = ['cart', 'item']

    # def clean(self, *args, **kwargs):
    #     if self.cart.paid_status == 1:
    #         super(ShoppingItems, self).clean(*args, **kwargs)
    #     else:
    #         raise ValidationError('Item has already been paid for')
    
    # def delete(self, *args, **kwargs):
    #     if self.cart.paid_status == 1:
    #         raise ValidationError('Item has already been paid for')
    #     else:
    #         super(ShoppingItems, self).delete(*args, **kwargs)