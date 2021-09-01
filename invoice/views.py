from django.shortcuts import render
import json
from accounts import models as Accounts
from products import models as Products
from invoice import models as Invoices
from market import models as Markets
from users import models as Users
from invoice.serializer import ItemSerializer


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
        cart = invoice.order_no

    elif order_id is not None:
        cart = Markets.ShoppingCart.objects.get(id=order_id)
        customer = cart.customer
        try:
            invoice = Invoices.salesInvoice.objects.filter(order_no=order_id)[0]
            items = Invoices.salesItem.objects.filter(salesInvoice=invoice)
        except:
            invoice = Invoices.salesInvoice(issued_for=customer, issued_by=request.user)
            items = Markets.ShoppingItems.objects.filter(cart__id=order_id)
        owner = Users.UserType.objects.get(user=request.user).belongs_to_dealer


    else:
        customer = Accounts.Customer.objects.get(id=customer_id)
        owner = Users.UserType.objects.get(user=request.user).belongs_to_dealer
        invoice = Invoices.salesInvoice(issued_for=customer, issued_by=request.user)

    context = {
        'customer': customer, 
        'items_list': json.dumps(items_list),
        'items': items,
        'invoice': invoice,
        'owner': owner,
        'cart': cart,
        "unsaved": True,
        "due" : round(customer.arthik_remaining_pay, 2),
        'order': cart
    }

    if request.method == "POST":
        data = request.POST
        items_post = json.loads(data['items'])
        invoiceDetails = json.loads(data['invoice'])
        try:
            invoice.total = invoiceDetails['total']
            invoice.tax = invoiceDetails['tax']
            invoice.paid_amount = invoiceDetails['paid']
            invoice.date = invoiceDetails['date']
            invoice.discount = invoiceDetails['discount']
            invoice.to_pay = invoiceDetails['to_pay']
            invoice.notes = invoiceDetails['notes']
            invoice.is_posted = True
            invoice.vat_bill_no = invoiceDetails['vat']
            invoice.order_no = cart
            invoice.save()
            invoice = Invoices.salesInvoice.objects.get(id=invoice.id)
        except:
            context["errors"]= "Error in Details of Invoice"
            return(request, 'cashflow/invoice.html', context)

        items = Invoices.salesItem.objects.filter(salesInvoice=invoice)
        already_saved_ids = items.values_list('id', flat=True)
        saved_items_id = []
        for posted_item in items_post:
            posted_item['salesInvoice'] = invoice.id
            if posted_item['id'] == "":
                item_save = ItemSerializer(data=posted_item)
            else:
                item_saved = Invoices.salesItem.objects.get(id=posted_item["id"])
                item_save = ItemSerializer(instance=item_saved, data=posted_item)
            if item_save.is_valid():
                item_saved = item_save.save()
            else:
                context.update({
                        "errors":"Error in Item " + posted_item['description']
                    })
                return(request, 'cashflow/invoice.html', context)

            saved_items_id.append(item_saved.id)

        to_delete = list(
            set(already_saved_ids) - set(saved_items_id)
        )
        Invoices.salesItem.objects.filter(id__in = to_delete).delete()
        items = Invoices.salesItem.objects.filter(salesInvoice=invoice)
        context.update({
        "id" : id,
        "invoice": invoice,
        "user": request.user,
        "owner": owner,
        "items": items,
        "customer" : customer,
        "unsaved": False,
        "due" : customer.remaining_pay(),
        'order':cart
        })
        return render(request, 'cashflow/invoice.html', context)

    return render(request, template_name="cashflow/invoice.html", context=context)
