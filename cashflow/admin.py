from django.apps import apps
from django.contrib import admin
from django.urls import reverse, resolve
from django.utils.html import format_html
from nepali_date import NepaliDate
from invoice.admin import InvoiceInline


class PaymentInline(admin.TabularInline):
    model = apps.get_model('cashflow', model_name='Payment')
    extra = 1
    show_change_link = True
    ordering = ('-date',)
    fields = ['nepali_date', 'amount', 'payment_mode', 'nep_date', 'date', 'term']
    readonly_fields = ['nep_date',]

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


class OpeningInline(admin.TabularInline):
    model = apps.get_model('cashflow', model_name='OpeningBalance')
    # fields = '__all__'
    extra = 0
    show_change_link = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        UserMode = apps.get_model('users', model_name='UserSystem')
        if UserMode.objects.get(user=request.user).default_term == 1:
            return qs
        a,b, object_id = resolve(request.path)
        op_bal = apps.get_model('cashflow', model_name='OpeningBalance')
        try:
            op_bal_reqd = op_bal.objects.filter(customer__id = object_id['object_id']).order_by('-term__start_date')[0]
            return qs.filter(id=op_bal_reqd.id)
        except:
            return qs



@admin.register(apps.get_model('accounts', model_name='Customer'))
class CustomerAdmin(admin.ModelAdmin):
    model = apps.get_model('accounts', model_name='Customer')
    ordering = ('name',)
    list_display = ['name', 'phone', 'pan', 'address', 'remaining_pay', 'arthik_pending']
    inlines = [InvoiceInline, PaymentInline, OpeningInline]
    readonly_fields = ('addInvoice', )
    search_fields = ('name','address', 'phone','pan')
    classes = ('extrapretty',)
    admin_order_field = ('remaining_pay',)
    fieldsets = (
        (None,
            { "fields": ('name', 'addInvoice' ),
            "classes": ["tab-basic",],}
        ),
        ("Other Details",
            {
            'classes': ('collapse', "other"),
            "fields": ("contact_person", "phone", "pan", "address", )
            }
        )
    )
    save_on_top = True
    tabs = [
        ("Payment", ["tab-payment-inline",]),
        ("Invoices", ["tab-invoice-inline",]),
        ("Opening", ["tab-opening-inline",]),
        ("Basic Info", ["tab-basic", "other"])
    ]


    def addInvoice(self, obj):
        try:
            return format_html("<a class='button' href='%s'>Add New Invoice</a>" % reverse('invoice:cs_id', kwargs={"customer_id":obj.id}))
        except:
            return "Save the customer first"


@admin.register(apps.get_model('cashflow', model_name='OpeningBalance'))
class OpeningAdmin(admin.ModelAdmin):
    list_display = ['account', 'closing_due', 'term']
    readonly_fields = [ 'closing_due', 'term_start', 'term_end', 'print_statement', 'term', 'print_monthly_statement']
    list_filter = ['account__name', 'term']
    search_fields = ('account__name',)


    def print_statement(self,obj):
        return format_html("<a href='%s' target='_blank' class='button'>Open Statement</a>" % reverse('cashflow:opening_details', kwargs= {"id":obj.id}))
    
    def print_monthly_statement(self, obj):
        return format_html("<a href='%s' target='_blank' class='button'>Open Monthly Statement</a>" % reverse('cashflow:customer_month_details', kwargs= {"id":obj.account.id, "term": obj.term.id}))

register_models = ['Term', 'OpeningBalanceDealer',]

for x in register_models:
    my_model = apps.get_model('cashflow', model_name=x)
    admin.site.register(my_model)
