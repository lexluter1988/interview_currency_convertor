# -*- coding: utf-8 -*-

from rest_framework import serializers

from models import CurrencyData


class CurrencyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyData
        fields = ('id', 'updated', 'full_name', 'short_name', 'exchange_rate')


class InputSerializer(serializers.Serializer):
    currency_from = serializers.CharField()
    currency_to = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=10)