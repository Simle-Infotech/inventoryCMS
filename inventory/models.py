from datetime import time
from django.db import models
from django.utils import timezone
from django.apps import apps
from datetime import date
import numpy as np


class openingInventory(models.Model):
    product = models.ForeignKey('products.ItemColorAvailability', on_delete=models.CASCADE)
    opening_qty = models.FloatField("Opening Quantity")
    rate = models.FloatField("Opening Rate")
    expiry = models.DateField("Expiry Date", default=timezone.now)
    entry_date = models.DateField(default=timezone.now)
    entry_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    original_expiry_date = None
    original_qty = None

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.original_expiry_date = self.expiry
            self.original_qty = self.opening_qty


    def __str__(self):
        return "%s: %.0f on %s" % (self.product, self.opening_qty, self.entry_date)
    
    def save(self, *args, **kwargs):
        # Cases 
        '''
        1. If expiringItem already Exists:
            1.1 If this is new Save:
                Add opening Qty to Expiring Count
            1.2 Else: this is updating existing OpeningInventory Count
                previous ExpiringDate Exists in ExpiringItems
                Reduce the no. of previous Qty count from the associated ExpiringItem
                Try Adding to Existent ExpiringItem
        2. Else expiringItem has to be created:
            2.1 If this is new save:
                Add opening Qty to Expiring Count
            2.2 Else: 
                previous ExpiringDate Exists in ExpiringItems
                Reduce the no. of previous Qty count from the associated ExpiringItem
                Try Adding to new ExpiringItem object

        
        '''
        
        ExpiringClass = apps.get_model(app_label='inventory', model_name="ExpiringItems")
        expiringItem, created = ExpiringClass.objects.get_or_create(product=self.product, date = self.expiry)
        if self.id:
                prevExpiringItem = ExpiringClass.objects.get(product=self.product, date = self.original_expiry_date)
                prevExpiringItem.qty -= self.original_qty
                prevExpiringItem.save()
                expiringItem.qty += self.opening_qty
                expiringItem.save()
        else:
                expiringItem.qty += self.opening_qty
                expiringItem.save()

        super(openingInventory, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs) :
        ExpiringClass = apps.get_model(app_label='inventory', model_name="ExpiringItems")
        prevExpiringItem = ExpiringClass.objects.get(product=self.product, date = self.original_expiry_date)
        prevExpiringItem.qty -= self.original_qty
        return super().delete(*args, **kwargs)
    
    class Meta:
        unique_together = ('product',)
        ordering = ['-entry_date',]


def find_rate(opening, sales, purchases):
    purchase_rate = 0
    salesQty = sum(sales.values_list('qty', flat=True))
    purchaseQty = purchases.values_list('qty', flat=True)
    cumulative = opening.rate * opening.opening_qty
    cum_qty = opening.opening_qty
    cumsumPurchase = np.cumsum(purchaseQty) + cum_qty
    relevant_purchases = np.extract(purchases, [ cumsumPurchase > salesQty] )
    if np.sum(salesQty == cumsumPurchase):
        active_stock_from_purchase = 0
    else:
        active_stock_from_purchase = np.extract( cumsumPurchase > salesQty, cumsumPurchase)[0] - salesQty
    
    flag = True
    for x in relevant_purchases:
        if flag:
            x.qty += -active_stock_from_purchase
            balance = x.qty
            flag = False
        cumulative += x.qty * x.rate
        cum_qty += x.qty
    
    if len(relevant_purchases == 0):
        relevant_purchases = [None,]
        balance = cum_qty
    
    return {'rate': cumulative / cum_qty, 'purchase': relevant_purchases[0], 'balance': balance}
    

class InventoryCount(models.Model):
    product = models.OneToOneField('products.ItemColorAvailability', on_delete=models.CASCADE)
    count = models.FloatField("Existing Qty", default=0)
    rate = models.FloatField("Current Rate", default=0)
    count_updated_date = models.DateField("Count Date", auto_now=True)
    current_opening = models.ForeignKey('inventory.openingInventory', blank=True, null=True, on_delete=models.SET_NULL)
    ## Managed in separate Expiry Dates Section
    # expiry_date = models.DateField(default=timezone.now) -- expiry date of current_purchase_pointer
    # current_purchase_pointer = models.OneToOneField('invoice.purchaseItem', on_delete=models.SET_NULL, blank=True, null=True)
    # has_error = models.BooleanField(default=False)
    # balance = models.FloatField(default=0)
    
    
    def update_count(self):
        salesItem = apps.get_model('market', model_name="salesItem")
        purchaseItem = apps.get_model('market', model_name="purchaseItem")
        opening_qtys = openingInventory.objects.filter(product = self.product)
        if len(opening_qtys) == 0:
            opening_qty = openingInventory.objects.create(product = self.product, opening_qty = 0, rate = 0, entry_date = date.fromisocalendar(2001, 1, 1))
            open = opening_qty.opening_qty
        else:
            opening_qty = opening_qtys[0]
            open = opening_qty.opening_qty
            more = opening_qtys.filter(count_updated_date=opening_qty.count_updated_date)
            if len(more) > 1:
                # Same day opening Qty... (Probably different expiry dates need to work on it)
                open = sum(more.values_list('opening_qty', flat=True))
        self.current_opening = opening_qty
        sales = salesItem.objects.filter(product=self.product, salesinvoice__date__gte=opening_qty.entry_date).order_by('salesinvoice__date')
        purchases = purchaseItem.objects.filter(product=self.product, purchaseinvoice__date__gte=opening_qty.entry_date).order_by('purchaseinvoice__date')
        self.count = open - sum(sales.values_list('qty', flat=True)) + sum(purchases.values_list('qty', flat=True))
        self.count_updated_date = date.today()
        result = find_rate(opening_qty, sales, purchases)
        self.rate = result['rate']
        # self.current_purchase_pointer = result['purchase']
        # self.balance = result['balance']
        self.save()

    class Meta:
        unique_together = ('product',)


class ExpiringItems(models.Model):
    product = models.ForeignKey('products.ItemColorAvailability', on_delete=models.CASCADE)
    date = models.DateField('Expiry Date', null=True, blank=True)
    qty = models.FloatField('Quantity', default=0)

    class Meta:
        unique_together=('product', 'date')
        ordering = ['date']
    
