from rest_framework import serializers

from .models import *


class VisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visa
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    visas = VisaSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'