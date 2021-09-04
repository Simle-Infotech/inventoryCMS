"""fEN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from cashflow import views as CashView

urlpatterns = [
    path('opbal/<int:id>/', CashView.customer_details, name='opening_details'),
    path('opbal/<int:id>/term/<int:term>/',CashView.monthly_details, name="customer_month_details"),
    path('opbal/term/<int:term>', CashView.term_monthly_details, name="term_monthly"),
] 

app_name = "cashflow"