from fEN.settings import TOTAL_WITH_TAX
from django.apps import apps
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, resolve
from django.conf import settings
from django.contrib.auth.models import User, Group
from inline_actions.admin import InlineActionsMixin
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from nepali_date.date import NepaliDate
from django.db.models import Sum, Q, F, Value


# class ContactPersonInline(admin.StackedInline):
#     model = apps.get_model('accounts', model_name='Person')
#     show_change_link = True
#     exclude = ('contact_person',)
    # fields = ['nepali_date', 'amount', 'payment_mode', 'nep_date', 'date', 'term']
    # readonly_fields = ['nep_date',]

class ItemsCartAdmin(admin.TabularInline):
    model = apps.get_model('market', model_name="ShoppingItems")
    show_change_link = True
    exclude = ('price', 'taxable', 'tax_included' )
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.exclude = []
        return super( ItemsCartAdmin, self).get_formset( request, obj, **kwargs)



@admin.register(apps.get_model('market', model_name='ShoppingCart'))
class ShoppingCartAdmin(admin.ModelAdmin):
    model = apps.get_model('market', model_name='ShoppingCart')
    exclude = ['customer', 'paid_status']
    list_display = ['__str__','customer', 'paid_status', 'total']
    inlines = [ItemsCartAdmin, ]
    readonly_fields = ['total', 'total_tax']


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            self.exclude = ['customer',]
            self.list_filter = ['customer', 'paid_status']
            return qs
        else:
            self.list_display = ['__str__', 'paid_status', 'total']
        return qs.filter(customer=request.user.usertype.belongs_to_customer)

    def save_model(self, request, obj, form, change):
        obj.customer = request.user.usertype.belongs_to_customer
        obj.save()
    
    def total(self, obj):
        items = obj.shoppingitems_set.all()
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
    
    def total_tax(self, obj):
        items = obj.shoppingitems_set.all()
        mytotal = 0
        # Tax Included Items
        tax_inc_items = items.filter(Q(Q(taxable = True) & Q(tax_included = True)))
        if tax_inc_items.count()>0:
            mytotal += tax_inc_items.aggregate(
                total = Sum(F('price') * F('qty'))
            )['total'] / settings.TOTAL_WITH_TAX * TAX

        tax = items.filter(taxable=True) 
        if tax.count()>0:
            mytotal += tax.aggregate(
                total = Sum(F('price') * F('qty'))
            )['total'] * settings.TAX
        
        return mytotal

    
    def get_fieldsets(self, request, obj):
        return super().get_fieldsets(request, obj=obj)

    