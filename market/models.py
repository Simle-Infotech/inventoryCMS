from django.db.models import Sum, Q, F, Value
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import logging
from django.forms.models import model_to_dict
logger = logging.getLogger('Shopping.cart')
from notifications.signals import notify
from django.contrib.auth.models import User


class ShoppingCart(models.Model):
    # order = models.ForeignKey('market.MarketOrder', on_delete=models.CASCADE)
    customer = models.ForeignKey('accounts.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    paid_choices = (
        (1, "Unpaid"),
        (2, "Paid in Cash"),
        (3, "Paid in Cheque"),
        (4, "Free Distribution"),
        (5, "Marked for Delivery")
    )
    paid_status = models.IntegerField(choices=paid_choices, default=1)
    description = models.TextField(blank=True, null=True)
    # total = models.FloatField(default=0.0)
    # total_tax = models.FloatField(default=0.0)
    cart_created = models.DateTimeField(auto_now_add=True )

    def __str__(self):
        if self.description is not None:
            return self.description
        else:
            return "%s : Cart" % (self.id)
    
    def save(self, *args, **kwargs):
        # self.total = self.get_total
        # self.total_tax = self.get_total_tax
        # logger.info(str(model_to_dict(self)))
        if self.paid_status != 1:
            notify.send(sender=User.objects.filter(is_superuser=True).first(), recipient=self.customer.usertype_set.get().user, target=self, verb="Order", description=dict(self.paid_choices)[self.paid_status])
            super(ShoppingCart, self).save(*args, **kwargs)
            return True
        
        if getattr(self, 'id', False):
            super(ShoppingCart, self).save(*args, **kwargs)
            notify.send(self.customer.usertype_set.get().user, recipient=User.objects.filter(is_superuser=True), verb="Order", description="Order Modified %s " % self.id, target=self)
        else:
            super(ShoppingCart, self).save(*args, **kwargs)
            notify.send(self.customer.usertype_set.get().user, recipient=User.objects.filter(is_superuser=True), verb="Order", description="Order Created %s " % self.customer.name, target=self)
            
        # return True

    
    # @property
    # def get_total(self):
    #     items = self.shoppingitems_set.all()
    #     mytotal = 0
    #     # Tax Included and Tax Excluded Items (Rate * Quantity)
    #     tax_inc_items = items.filter(Q(Q(taxable = True) & Q(tax_included = True)) | Q(taxable=False))
    #     if tax_inc_items.count()>0:
    #         mytotal += tax_inc_items.aggregate(
    #             total = Sum(F('price') * F('qty'))
    #         )['total']
    #     tax = items.filter(taxable=True)
    #     if tax.count()>0:
    #         mytotal += tax.aggregate(
    #             total = Sum(F('price') * F('qty') * Value(settings.TOTAL_WITH_TAX))
    #         )['total']
        
    #     return mytotal
    
    # @property
    # def get_total_tax(self):
    #     items = self.shoppingitems_set.all()
    #     mytotal = 0
    #     # Tax Included Items
    #     tax_inc_items = items.filter(Q(Q(taxable = True) & Q(tax_included = True)))
    #     if tax_inc_items.count()>0:
    #         mytotal += tax_inc_items.aggregate(
    #             total = Sum(F('price') * F('qty'))
    #         )['total'] / settings.TOTAL_WITH_TAX * settings.TAX

    #     tax = items.filter(taxable=True) 
    #     if tax.count()>0:
    #         mytotal += tax.aggregate(
    #             total = Sum(F('price') * F('qty'))
    #         )['total'] * settings.TAX
        
    #     return mytotal

    class Meta:
        ordering = ('-cart_created','-paid_status',)


class ShoppingItems(models.Model):
    item = models.ForeignKey('products.ItemColorAvailability', on_delete=models.CASCADE)
    qty = models.IntegerField('Quantity')
    cart = models.ForeignKey('market.ShoppingCart', on_delete=models.CASCADE)
    price = models.FloatField('Rate', default=0)
    taxable = models.BooleanField(default=True)
    tax_included = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        logger.info(str(model_to_dict(self)))
        super(ShoppingItems, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['cart', 'item']
