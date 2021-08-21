from django.contrib import admin

# Register your models here.
from django.apps import apps

register_models = ['salesInvoice', 'purchaseInvoice']

for x in register_models:
    my_model = apps.get_model('invoice', model_name=x)
    admin.site.register(my_model)
