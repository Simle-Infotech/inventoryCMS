from django.apps import apps
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = apps.get_model(app_label="cashflow", model_name="Payment")
        fields = '__all__'


class DealerPaymentSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = apps.get_model(app_label="cashflow", model_name="DealerPayment")
        fields = '__all__'


class TermSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = apps.get_model(app_label="cashflow", model_name="Term")
        fields = '__all__'


class OpeningBalanceSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = apps.get_model(app_label="cashflow", model_name="OpeningBalance")
        fields = '__all__'


class OpeningBalanceDealerSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = apps.get_model(app_label="cashflow", model_name="OpeningBalanceDealer")
        fields = '__all__'

