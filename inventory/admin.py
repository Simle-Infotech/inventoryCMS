from django.contrib import admin

from django.apps import apps

register_models = ['openingInventory']

for x in register_models:
    my_model = apps.get_model('inventory', model_name=x)
    admin.site.register(my_model)
