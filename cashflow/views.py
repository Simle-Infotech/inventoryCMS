from django.shortcuts import render
import json
from accounts import models as Accounts
from products import models as Products
from invoice import models as Invoices
from market import models as Markets


def invoice(request, order_id=None, id=None, customer_id=None):
    items_ = Products.ItemColorAvailability.objects.all().prefetch_related('item', 'color')
    items = []
    items_list = []
    for x in items_:
        items_list.append({x.id: x.__str__()})

    if id is not None:
        items = Invoices.salesItem.objects.get(salesInvoice__id=id)
        invoice = Invoices.salesInvoice.objects.get(id=id).prefetch_related('issued_for')
        customer = invoice.issued_for

    elif order_id is not None:
        items = Markets.ShoppingItems.objects.filter(cart__id=order_id)
        cart = Markets.ShoppingCart.objects.get(cart__id=order_id).prefetch_related('customer')
        customer = cart.customer
        invoice = Invoices.salesInvoice(issued_for=customer)

    else:
        customer = Accounts.Customer.objects.get(id=customer_id)
        invoice = Invoices.salesInvoice(issued_for=customer)

    context = {
        'id': id,
        'invoice': invoice,
        'customer': customer,
        'items_list': json.dumps(items_list),
        'items': items
    }

    return render(request, template_name="cashflow/invoice.html", context=context)
