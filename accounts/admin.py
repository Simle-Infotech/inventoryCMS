from django.apps import apps
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, resolve
from django.conf import settings
from django.contrib.auth.models import User, Group
from inline_actions.admin import InlineActionsMixin
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from nepali_date.date import NepaliDate

register_models = ["Person"]

# class ContactPersonInline(admin.StackedInline):
#     model = apps.get_model('accounts', model_name='Person')
#     show_change_link = True
#     exclude = ('contact_person',)
    # fields = ['nepali_date', 'amount', 'payment_mode', 'nep_date', 'date', 'term']
    # readonly_fields = ['nep_date',]


@admin.register(apps.get_model('accounts', model_name='Dealer'))
class DealerAdmin(admin.ModelAdmin):
    model = apps.get_model('accounts', model_name='Dealer')
    ordering = ('name',)
    list_display = ['name', 'phone', 'pan', 'address']
    # inlines = [ContactPersonInline,]


for x in register_models:
    my_model = apps.get_model('accounts', model_name=x)
    admin.site.register(my_model)
