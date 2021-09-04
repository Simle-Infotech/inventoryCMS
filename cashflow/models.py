from django.db import models
from nepali_date import NepaliDate
from django.db.models import Q
from django.contrib.auth.models import User


class PaymentMeta(models.Model):
    amount = models.FloatField()
    payment_mode = models.IntegerField(choices = ((1, "Cheque"), (2, "Cash"), (3,"Bank Transfer"), (4, "Internet Payment"), (5, "Transport"), (6, "Bank Deposit"), (7, "Goods Returned"), (8, "Discount")))
    date = models.DateField(null=True, blank=True)
    nepali_date = models.CharField(blank=True, max_length=20, default = "")
    term = models.ForeignKey("Term", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "%s" % self.amount

    def save(self, *args, **kwargs):
        if self.nepali_date != "":
            self.date = NepaliDate.to_english_date(NepaliDate(*self.nepali_date.split('-')))
        super(Payment, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Payment(PaymentMeta):
    customer = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)


class DealerPaymnet(PaymentMeta):
    dealer = models.ForeignKey('accounts.Dealer', on_delete=models.CASCADE)


class Term(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class OpeningBalanceMeta(models.Model):
    account = models.ForeignKey("accounts.Customer", on_delete=models.CASCADE)
    amount = models.FloatField("Opening Balance") # blank=True, null=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)

    def __str__(self):
        return "%s : %s" % (self.account.name, self.amount)

    def save(self, *args, **kwargs):
        if self.id:
            super(OpeningBalance, self).save(*args, **kwargs)
        else:
            if self.amount == 0:
                self.amount = self.account.remaining_pay()
            super(OpeningBalanceMeta, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('account', 'term')
        abstract = True

    @property
    def term_start(self):
        return self.term.start_date

    @property
    def term_end(self):
        return self.term.end_date

    def invoices(self):
        return self.account.salesinvoice_set.filter(
                date__range=[self.term.start_date, self.term.end_date]
            )

    def payments(self):
        return self.account.payment_set.filter(
                (Q(date__range=[self.term.start_date, self.term.end_date]) & Q(term__isnull = True)) | Q(term = self.term)
            )

    @property
    def closing_due(self):
        return sum(self.account.salesinvoice_set.filter(
                date__range=[self.term.start_date, self.term.end_date]
            ).values_list("to_pay", flat=True)) - \
            sum(self.account.payment_set.filter(
                date__range=[self.term.start_date, self.term.end_date]
            ).values_list('amount', flat=True)) + \
            self.amount

    @property
    def total_sales(self):
        return sum(self.account.salesinvoice_set.filter(
                date__range=[self.term.start_date, self.term.end_date]
            ).values_list("to_pay", flat=True))

    @property
    def total_pay(self):
        return sum(self.account.payment_set.filter(
            date__range=[self.term.start_date, self.term.end_date]
        ).values_list('amount', flat=True))


class OpeningBalance(OpeningBalanceMeta):
    def payments_until(self, end_date):
        return self.account.payment_set.filter(
            (Q(date__range=[self.term.start_date, end_date]) & Q(term__isnull = True)) | Q(term = self.term)
        ).values_list('amount', flat=True)
    
    def sales_until(self, end_date):
        return self.account.salesinvoice_set.filter(
                date__range=[self.term.start_date, end_date]
            ).values_list("to_pay", flat=True)


class OpeningBalanceDealer(OpeningBalanceMeta):
    account = models.ForeignKey("accounts.Dealer", on_delete=models.CASCADE)
