# from fEN.settings import TOTAL_WITH_TAX
from django.apps import apps
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import messages
from accounts import models as Accounts
from products import models as Products
from invoice import models as Invoices
from market import models as Markets

from django.utils.html import format_html
from django.urls import reverse, resolve
# from django.conf import settings
# from django.contrib.auth.models import User, Group
# from inline_actions.admin import InlineActionsMixin
# from django.shortcuts import redirect
# from django.utils.translation import ugettext_lazy as _
# from django.utils.safestring import mark_safe
# from nepali_date.date import NepaliDate
# from django.db.models import Sum, Q, F, Value


# class ContactPersonInline(admin.StackedInline):
#     model = apps.get_model('accounts', model_name='Person')
#     show_change_link = True
#     exclude = ('contact_person',)
#     fields = ['nepali_date', 'amount', 'payment_mode', 'nep_date', 'date', 'term']
#     readonly_fields = ['nep_date',]

class ItemsCartAdmin(admin.TabularInline):
    model = apps.get_model('market', model_name="ShoppingItems")
    show_change_link = True
    exclude = ('price', 'taxable', 'tax_included' )
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.exclude = []
        return super(ItemsCartAdmin, self).get_formset( request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            if obj.paid_status != 1:
                return False
            else:
                return True
        else:
            return True

    def has_add_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def has_delete_permission(self, request, obj):
        return self.has_change_permission(request, obj)




@admin.register(apps.get_model('market', model_name='ShoppingCart'))
class ShoppingCartAdmin(admin.ModelAdmin):
    model = apps.get_model('market', model_name='ShoppingCart')
    exclude = ['customer', 'paid_status', 'cart_created', 'description']
    inlines = [ItemsCartAdmin, ]
    jazzmin_section_order = ("ItemsCartAdmin", "general",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            self.exclude = []
            self.list_filter = ['customer', 'paid_status']
            self.list_display = ['customer', 'paid_status', 'invoice']
            self.readonly_fields = ['invoice']
            return qs
        else:
            self.list_display = ['cart_created','__str__', 'paid_status', ]
            self.exclude = ['customer', 'paid_status', 'cart_created', 'description']
            self.list_filter = ['paid_status']
            # self.readonly_fields = ['total', 'total_tax']
        return qs.filter(customer=request.user.usertype.belongs_to_customer)

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.customer = request.user.usertype.belongs_to_customer
        obj.clean()
        obj.save()
    
    def invoice(self, obj):
        if obj is None:
            return "Not Ready for Invoice"
        href = "<a href=\"%s\"> Goto Invoice </a>"
        order_invoices = Invoices.salesInvoice.objects.filter(order_no = obj)
        if order_invoices.count() > 0:
            return format_html(href % reverse('invoice:invoice_id', kwargs={'id': order_invoices[0].id}))
        
        return format_html(href % reverse('invoice:order_id', kwargs={'order_id':obj.id}))

    # def has_delete_permission(self, request, obj):
    #     if obj.paid_status != 1:
    #         return False
    #     else:
    #         return True

    def delete_model(self, request, obj):
        if obj.paid_status == 1:
            return super().delete_model(request, obj)
        else:
            messages.error(request, "Cant delete the saved model")
            return False

    def delete_queryset(self, request, queryset):
        queryset = queryset.filter(paid_status = 1)
        messages.error(request, "There were paid items which could not be deleted")
        return super().delete_queryset(request, queryset)
