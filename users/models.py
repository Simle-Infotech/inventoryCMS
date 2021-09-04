from django.db import models
from django.contrib.auth.models import User
from accounts.models import Dealer as Owner


class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # name = models.CharField("User Type Name", max_length=100)
    # nep_name = models.CharField("युजरको किसिम, नेपालीमा", max_length=300)
    # description = models.TextField(blank=True, null=True)
    belongs_to_customer = models.ForeignKey('accounts.Customer', on_delete=models.SET_NULL, null=True, blank=True)
    belongs_to_dealer = models.ForeignKey('accounts.Dealer', on_delete=models.SET_NULL, null=True, blank=True)


class UserSystem(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    default_term = models.IntegerField(
        choices=((0, "Yes"), (1, "No")), default = 0
    )