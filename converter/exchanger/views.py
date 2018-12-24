#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import CurrencyData
from serializers import CurrencyDataSerializer, InputSerializer
from oexchangerateconnector import OpenExchangeRateConnector
from config import OPEN_EXCHANGE_RATES_API_KEY, DAYS_OF_INACTIVITY
from django.utils import timezone


@csrf_exempt
def currency_rate_list(request):
    if request.method == 'GET':
        rates = CurrencyData.objects.all()
        # if no data about exchange rates, let's fill the DB
        if len(rates) == 0:
            update_rates()
        # if rates are outdated more than 1 day, let's update them
        elif (timezone.now() - rates[0].updated).days >= DAYS_OF_INACTIVITY:
            CurrencyData.objects.all().delete()
            update_rates()

        rates = CurrencyData.objects.all()

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
def currency_convert(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InputSerializer(data=data)
        if serializer.is_valid():
            a = serializer.data['currency_from']
            b = serializer.data['currency_to']
            c = serializer.data['amount']

            c_from = CurrencyData.objects.get(short_name__exact=a)
            c_to = CurrencyData.objects.get(short_name__exact=b)

            result = Decimal(c) / c_from.exchange_rate * c_to.exchange_rate
            data = {c + ' ' + a: str(round(result, 6)) + ' ' + b}

            return JsonResponse(data, status=201)

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
