from django.contrib import admin
from django.apps import apps
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

admin.site.unregister(User)


class UserTypeInline( admin.StackedInline ):
    model = apps.get_model('users', model_name="UserType")


class UserAdmin(BaseUserAdmin):
    inlines=(UserTypeInline, )
    extra = 1

admin.site.register(User, UserAdmin)
