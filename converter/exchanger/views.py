#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import CurrencyData
from serializers import CurrencyDataSerializer
from oexchangerateconnector import OpenExchangeRateConnector
from config import OPEN_EXCHANGE_RATES_API_KEY


@csrf_exempt
def currency_rate_list(request):
    if request.method == 'GET':
        rates = CurrencyData.objects.all()
        if len(rates) == 0:
            # need to update
            update_rates()
        # elif outdated: need to update

        serializer = CurrencyDataSerializer(rates, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CurrencyDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def currency_rate_detail(request, pk):
    try:
        currency = CurrencyData.objects.get(pk=pk)
    except CurrencyData.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CurrencyDataSerializer(currency)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CurrencyDataSerializer(currency, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        currency.delete()
        return HttpResponse(status=204)


def update_rates():
    client = OpenExchangeRateConnector(OPEN_EXCHANGE_RATES_API_KEY)
    rates = client.get_all_rates()
    for rate in rates:
        data = CurrencyData(full_name=rate.full_name, short_name=rate.short_name, exchange_rate=rate.exchange_rate)
        data.save()
