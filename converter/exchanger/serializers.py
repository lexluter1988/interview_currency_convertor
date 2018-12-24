#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from models import CurrencyData


class CurrencyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyData
        fields = ('id', 'updated', 'full_name', 'short_name', 'exchange_rate')