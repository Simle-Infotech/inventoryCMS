from django.apps import apps
from django.contrib import admin
from inventory.admin import InventoryAdmin

allowed_list = ['Tags', 'Item', 'Image', "Color"]

for x in allowed_list:
    my_model = apps.get_model('products', model_name=x)
    admin.site.register(my_model)


@admin.register(apps.get_model('products', model_name='ItemColorAvailability'))
class ItemColorAdmin(admin.ModelAdmin):
    model = apps.get_model('products', model_name="ItemColorAvailability")
    inlines = [InventoryAdmin]
    list_display = ['__str__',]
    list_filter = ['item__name', 'color__name']
    