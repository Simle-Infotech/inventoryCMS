from numpy import product
from products.models import Item
from django.db import models
from django.apps import apps

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
        if self.bill_no is not None:
            self.is_vat = True
        else:
            self.is_vat = False
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
    original_qty = None
    original_expiry_date = None

    class Meta:
        abstract = True
    
    def __init__(*args, **kwargs):
        super(ItemsMeta, self).__init__(*args, **kwargs)
        self.original_qty = self.qty
        self.original_expiry_date = self.expiryDate

class salesItem(ItemsMeta):
    salesInvoice = models.ForeignKey('invoice.salesInvoice', on_delete=models.CASCADE)

    

    def update_count_pointer(self, count_obj, qty):
        difference = count_obj.balance - qty
        if difference < 0:
            count_obj.count -= count_obj.balance
            
            if count_obj.current_purchase_pointer:
                # Update Current Purchase Pointer
                # Update Current Purchase Pointer's Balance
                # Condition that next purchase pointer doesn't exist
                if (count_obj.current_purchase_pointer == count_obj.current_purchase_pointer.next_same_product_entry):
                    # error handle
                    pass
                else:
                    count_obj.current_purchase_pointer = count_obj.current_purchase_pointer.next_same_product_entry
                count_obj.balance = count_obj.current_purchase_pointer.qty
                self.update_count_pointer(count_obj, qty - count_obj.balance)
            else:
                # Items are being removed from Opening Balance
                y = self.__class__.objects.filter(salesinvoice__date__gte=count_obj.current_opening.entry_date, product = self.product)
                if y.count() > 0:
                    count_obj.current_purchase_pointer = y[0]
                else:
                    # No Items in Stock (Error)
                    pass
                count_obj.count -= count_obj.balance
                self.update_count_pointer(count_obj, qty - count_obj.balance)
                
                
            
            
            
        else:
            count_obj.count += -difference 
            count_obj.balance += -difference
            count_obj.save()


    def save(self, *args, **kwargs):
        if self.product:
            try:
                count_obj = self.product.inventorycount_set.get()
            except:
                Count = apps.get_model('inventory', model_name="InventoryCount")
                count_obj = Count(product=self.product, count=0, rate=0)
                count_obj.save()
                count_obj.update_count()
            self.update_count_pointer(count_obj, self.qty)
            
        super(salesItem, self).save(*args, **args)
        

    class Meta:
        ordering = ['salesInvoice__date']



class purchaseItem(ItemsMeta):
    purchaseInvoice = models.ForeignKey('invoice.purchaseInvoice', on_delete=models.CASCADE)

    def next_same_product_entry(self, opening=False):
        try:
            return self.__class__.objects.filter(product=self.product, purchaseinvoice__date__gte=self.purchaseInvoice.date)[1]
        except:
            return self
        


    class Meta:
        ordering = ['purchaseInvoice__date']
