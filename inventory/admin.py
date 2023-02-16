from django.contrib import admin

from django.apps import apps

register_models = []

for x in register_models:
    my_model = apps.get_model('inventory', model_name=x)
    admin.site.register(my_model)

class InventoryAdmin(admin.TabularInline):
    model = apps.get_model('inventory', model_name="openingInventory")
    exclude = ('entry_by',)
    extra = 1

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.entry_by = request.user
        obj.clean()
        obj.save()


