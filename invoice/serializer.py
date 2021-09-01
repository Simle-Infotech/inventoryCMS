from rest_framework import serializers
from .models import salesItem

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = salesItem
        fields = "__all__"
