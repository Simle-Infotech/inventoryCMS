from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField("User Type Name", max_length=100)
    # nep_name = models.CharField("युजरको किसिम, नेपालीमा", max_length=300)
    # description = models.TextField(blank=True, null=True)
    belongs_to_customer = models.ForeignKey('accounts.Customer', on_delete=models.SET_NULL, null=True, blank=True)
