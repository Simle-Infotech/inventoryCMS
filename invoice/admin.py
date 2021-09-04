from django.contrib import admin
from inline_actions.admin import InlineActionsMixin
from django.urls import reverse, resolve
from django.utils.safestring import mark_safe
from nepali_date.date import NepaliDate

# Register your models here.
from django.apps import apps

register_models = ['salesInvoice', 'purchaseInvoice']

for x in register_models:
    my_model = apps.get_model('invoice', model_name=x)
    admin.site.register(my_model)


class InvoiceInline(admin.TabularInline, InlineActionsMixin):
    model = apps.get_model('invoice', model_name='salesInvoice')
    fields = ('Invoice','nep_date','is_posted', 'to_pay', 'total', 'tax', 'bill_no', 'is_vat')
    extra = 1
    show_change_link = True
    inline_actions = ['view']
    readonly_fields = ['Invoice', 'nep_date']
    ordering = ('-date',)

    def url(self,obj):
        if obj.id:
            return reverse('invoice:invoice_id', kwargs={"id": obj.id})
        else:
            return reverse('invoice:cs_id', kwargs={ "customer_id":obj.issued_for.id})

    def Invoice(self, obj):
        return mark_safe("<a href=\"%s\"> View </a>" % self.url(obj) )

    def get_form(self, request, obj=None, **kwargs):
        form = super(InvoiceInline, self).get_form(request, obj, **kwargs)
        form.base_fields['user'] = request.user
        return form

    def nep_date(self, obj):
        try:
            # valid_dob = (self.date.split('-'))
            return NepaliDate.to_nepali_date(obj.date)
        except:
            return '-'
        return

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        UserMode = apps.get_model('users', model_name='UserSystem')
        if UserMode.objects.get(user=request.user).default_term == 1:
            return qs
        a,b, object_id = resolve(request.path)
        op_bal = apps.get_model('cashflow', model_name='OpeningBalance')
        try:
            op_bal_reqd = op_bal.objects.filter(customer__id = object_id['object_id']).order_by('-term__start_date')[0]
            return qs.filter(date__gte = op_bal_reqd.term.start_date)
        except:
            return qs


    # def view(self, request, obj, parent_obj=None):
    #     url = "/hello"
    #     return redirect(url)
    # view.short_description = "Generate Items"


class salesInvoiceAdmin(admin.ModelAdmin):
    model = apps.get_model('invoice', model_name='salesInvoice')

admin.register(salesInvoiceAdmin.model, salesInvoiceAdmin)

class purchaseInvoiceInline(InvoiceInline):
    model = apps.get_model('invoice', model_name='purchaseInvoice')

    def Invoice(self, obj):
        return True

class purchaseItemInline(admin.TabularInline, InlineActionsMixin):
    model = apps.get_model('invoice', model_name='purchaseItem')
    inline_actions = ['view']
