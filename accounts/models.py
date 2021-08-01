from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=200)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class CustomerMeta(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    pan = models.IntegerField(null=True, blank=True)
    contact_person = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


    class Meta:
        abstract = True


class Dealer(CustomerMeta):
    pass


class Customer(CustomerMeta):

    def addInvoice(self):
        return "<a class=\"button\" href=\"%s\" target='_blank'>Add Invoice</a>" % reverse('invoices:index_id_csid', kwargs={"id": 0, "cs_id":pk})

    # @property
    def remaining_pay(self):
        try:
            return round(
                sum(self.invoice_set.all().values_list("to_pay", flat=True)) - \
                sum(self.payment_set.all().values_list('amount', flat=True)) + \
                self.openingbalance_set.all().prefetch_related('term').order_by('term__start_date')[0].amount,
            2)
                # sum(self.openingbalance_set.all().values_list('amount', flat=True))
        except:
            return round(
                sum(self.invoice_set.all().values_list("to_pay", flat=True)) - \
                sum(self.payment_set.all().values_list('amount', flat=True)),
            2)

    @property
    def arthik_remaining_pay(self):
        try:
            open_bal = self.openingbalance_set.all().prefetch_related('term').order_by('-term__start_date')[0]
            return round(
                sum(self.invoice_set.filter(date__gte = open_bal.term.start_date).values_list("to_pay", flat=True)) - \
                sum(self.payment_set.filter(date__gte = open_bal.term.start_date).filter(
                Q(term__isnull=True) | Q(term = open_bal.term.id)
                ).values_list('amount', flat=True)) + \
                open_bal.amount,
            2)
        except:
            return round(
                sum(self.invoice_set.all().values_list("to_pay", flat=True)) - \
                sum(self.payment_set.all().values_list('amount', flat=True)),
            2)