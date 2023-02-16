from django.apps import apps
from django.db.models import signals

"""
 --- Counts Will be
Items can be
    1. Fresh Purchase -- New Subtract
    2. Purchase Modified -- Prev. Add, New Subtract
    3. Purchase Deleted -- Reduce 
    4. Fresh Sales -- New Add
    5. Sales Modified -- Prev.. Subtract, New Add
    6. Sales Deleted -- Add
"""
ExpiringItem = apps.get_model(app_label='inventory', model_name="ExpiringItems")
PurchaseItem = apps.get_model(app_label='invoice', model_name="PurchaseItem")
salesItem = apps.get_model(app_label='invoice', model_name="PurchaseItem")

# def count_expiring_sales()