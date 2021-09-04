from django.shortcuts import render
import json
from accounts import models as Accounts
from products import models as Products
from invoice import models as Invoices
from market import models as Markets
from cashflow import models as CashFlows
from nepali_date.date import NepaliDate
from django.db.models import  Q
import pandas as pd
import nepali_datetime


def customer_details(request,id):
    openBal =CashFlows.OpeningBalance.objects.get(id=id)


    context = {
        "title": "%s-%s" %(openBal.account.name , openBal.term.title),
        "invoices": openBal.invoices,
        "payments": openBal.payments,
        "opening": openBal
    }
    return render (request, 'cashflow/customer_details.html', context=context)


def monthly_details(request, id, term): 
    customer = Accounts.Customer.objects.get(id =id)
    opening = CashFlows.OpeningBalance.objects.get(term__id = term, account = customer)
    nep_start = NepaliDate.to_nepali_date(opening.term.start_date)
    nep_end = NepaliDate.to_nepali_date(opening.term.end_date)
    if NepaliDate.today()< nep_end:
        nep_end = NepaliDate.today()
    all_calendar = pd.read_csv(nepali_datetime.calendar_file.name, index_col = 0)
    
    current_year = int(nep_start.year)
    current_month = int(nep_start.month)
    i = True
    titles = []
    openings = []
    sales = []
    payments = []
    id_tags = []
    opening_dates = []

    while (i):
        if current_month == 1:
            prev_month = 12
            prev_year = current_year - 1
        else:
            prev_month = current_month - 1
            prev_year = current_year

        
        year_calendar = all_calendar.loc[current_year]
        titles.append('%s:%s' % (current_year, year_calendar.index[current_month-1]))
        month_days = int(year_calendar[current_month-1])
        prev_month_days = int(year_calendar[prev_month-1])
        
        start_day = NepaliDate(prev_year, prev_month, prev_month_days).to_english_date()
        end_day = NepaliDate(current_year, current_month, month_days).to_english_date()
        opening_dates.append(start_day)
        monthly_opening = opening.amount + sum(opening.sales_until(start_day)) - sum(opening.payments_until(start_day))
        monthly_invoices = Invoices.salesInvoice.objects.filter(
            Q(date__gte = start_day) & Q(date__lte = end_day) & Q(issued_for=customer)
        )
        monthly_payments = CashFlows.Payment.objects.filter(
            Q(date__gte=start_day) & Q(date__lte=end_day) & Q(Q(term__isnull=True) | Q(term__id=term)) & Q(customer=customer)
        )
        
        i, current_month, current_year = update_loop(i, current_month, current_year, nep_end)
        openings.append(monthly_opening)
        sales.append(monthly_invoices)
        payments.append(monthly_payments)
        id_tags.append('%s%s'%(current_year, current_month))

    context = {
        'page_title': customer.name,
        'titles':titles, 'openings': openings, 'sales': sales, 'debits':payments, 'ids': id_tags,
        # 'titles_ids': zip(titles, id_tags),
        'accounts': zip(id_tags, openings, opening_dates, sales, payments, titles),
    }
    return render(request, 'cashflow/monthly_details.html', context=context)


def update_loop(i, current_month, current_year, nep_end):
    if (current_year == nep_end.year) & (current_month == nep_end.month):
        i = False
    if current_month == 12:
        current_month = 1
        current_year += 1
    else:
        current_month += 1
    return i, current_month, current_year


def term_monthly_details(request, term):
    opening_bals = CashFlows.OpeningBalance.objects.filter(term__id = term)
    opening_term = CashFlows.Term.objects.get(id=term)
    monthly_opening = sum(opening_bals.values_list('amount', flat=True))
    nep_start = NepaliDate.to_nepali_date(opening_term.start_date)
    nep_end = NepaliDate.to_nepali_date(opening_term.end_date)
    if NepaliDate.today()< nep_end:
        nep_end = NepaliDate.today()
    all_calendar = pd.read_csv(nepali_datetime.calendar_file.name, index_col = 0)
    
    current_year = int(nep_start.year)
    current_month = int(nep_start.month)
    i = True
    titles = []
    openings = []
    sales = []
    payments = []
    id_tags = []
    opening_dates = []
    cash_payments = []

    while (i):
        if current_month == 1:
            prev_month = 12
            prev_year = current_year - 1
        else:
            prev_month = current_month - 1
            prev_year = current_year

        
        year_calendar = all_calendar.loc[current_year]
        titles.append('%s:%s' % (current_year, year_calendar.index[current_month-1]))
        month_days = int(year_calendar[current_month-1])
        prev_month_days = int(year_calendar[prev_month-1])
        
        start_day = NepaliDate(current_year, current_month, 1).to_english_date()
        end_day = NepaliDate(current_year, current_month, month_days).to_english_date()
        opening_dates.append(start_day)
        monthly_invoices = Invoices.salesInvoice.objects.filter(
            Q(date__gte = start_day) & Q(date__lte = end_day) 
        ).prefetch_related('issued_for')
        monthly_payments = CashFlows.Payment.objects.filter(
            Q(date__gte=start_day) & Q(date__lte=end_day) & Q(Q(term__isnull=True) | Q(term__id=term))
        ).prefetch_related('customer')
        
        i, current_month, current_year = update_loop(i, current_month, current_year, nep_end)
        openings.append(monthly_opening)
        monthly_opening += sum(monthly_invoices.values_list('total', flat=True)) - sum(monthly_payments.values_list('amount', flat=True)) - sum(monthly_invoices.values_list('paid_amount', flat=True))
        sales.append(monthly_invoices)
        payments.append(monthly_payments)
        id_tags.append('%s%s'%(current_year, current_month))
        cash_payments.append({'amount':sum(monthly_invoices.values_list('paid_amount', flat=True)), 'date': end_day})

    context = {
        'page_title': "Monthly Summary",
        'titles':titles, 'openings': openings, 'sales': sales, 'debits':payments, 'ids': id_tags,
        'titles_ids': zip(titles, id_tags),
        'accounts': zip(id_tags, openings, opening_dates, sales, payments, titles, cash_payments), 
    }
    return render(request, 'cashflow/monthly_details_term.html', context=context)
