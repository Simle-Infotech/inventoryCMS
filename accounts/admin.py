from django.contrib import admin
from django.apps import apps

register_models = ['Customer', 'Dealer']

for x in register_models:
    my_model = apps.get_model('accounts', model_name=x)
    admin.site.register(my_model)
