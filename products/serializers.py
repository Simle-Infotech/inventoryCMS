from django.apps import apps
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model(app_label="products", model_name='Image')
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model(app_label="products", model_name='Tags')
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model(app_label="products", model_name='Item')
        fields = '__all__'
