from django.shortcuts import render
import json
from accounts import models as Accounts
from products import models as Products
from invoice import models as Invoices
from market import models as Markets
from users import models as Users


def invoice(request, order_id=None, id=None, customer_id=None):
    items_ = Products.ItemColorAvailability.objects.all().prefetch_related('item', 'color')
    items = []
    items_list = []
    cart = Markets.ShoppingCart()
    for x in items_:
        items_list.append({x.id: x.__str__()})
        
    if id is not None:
        items = Invoices.salesItem.objects.get(salesInvoice__id=id)
        invoice = Invoices.salesInvoice.objects.get(id=id)
        customer = invoice.issued_for
        owner = invoice.issued_by.usertype.belongs_to_dealer

    elif order_id is not None:
        items = Markets.ShoppingItems.objects.filter(cart__id=order_id)
        cart = Markets.ShoppingCart.objects.get(id=order_id)
        customer = cart.customer
        invoice = Invoices.salesInvoice(issued_for=customer)
        owner = Users.UserType.objects.get(user=request.user).belongs_to_dealer


    else:
        customer = Accounts.Customer.objects.get(id=customer_id)
        owner = Users.UserType.objects.get(user=request.user).belongs_to_dealer
        invoice = Invoices.salesInvoice(issued_for=customer)

    context = {
        'customer': customer, 
        'items_list': json.dumps(items_list),
        'items': items,
        'invoice': invoice,
        'owner': owner,
        'cart': cart
    }
    return render(request, template_name="cashflow/invoice.html", context=context)
