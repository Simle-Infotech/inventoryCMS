from django.apps import apps
from django.contrib import admin

allowed_list = ['Tags', 'Item']

# for x in apps.get_models():
#     for r in allowed_list:
#         if r in str(x):
#             try:
#                 admin.site.register(x)
#             except:
#                 pass

for x in allowed_list:
    my_model = apps.get_model('products', model_name=x)
    admin.site.register(my_model)
