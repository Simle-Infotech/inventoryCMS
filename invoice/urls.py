from django.urls import path, include
import invoice.views as Views

urlpatterns = [
  path('id/<int:id>', Views.invoice, name="invoice_id"), 
  path('csid/<int:customer_id>', Views.invoice, name="cs_id"),
  path('orderid/<int:order_id>', Views.invoice, name="order_id"),  
]

app_name = 'invoice'
