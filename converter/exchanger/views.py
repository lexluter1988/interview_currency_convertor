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
from config import OPEN_EXCHANGE_RATES_API_KEY, DAYS_OF_INACTIVITY, CURRENCY_PRECISION
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def currency_rate_list(request):
    """
    Getting all Currencies with rates and latest update time.
    """
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
        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def currency_convert(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InputSerializer(data=data)
        if serializer.is_valid():
            try:
                result = make_exchange(serializer.data)
            except CurrencyData.DoesNotExist:
                Response(status=status.HTTP_404_NOT_FOUND)
            return Response(result)

        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@csrf_exempt
def currency_rate_detail(request, pk):
    try:
        currency = CurrencyData.objects.get(pk=pk)
    except CurrencyData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CurrencyDataSerializer(currency)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def update_rates():
    client = OpenExchangeRateConnector(OPEN_EXCHANGE_RATES_API_KEY)
    rates = client.get_all_rates()
    for rate in rates:
        data = CurrencyData(full_name=rate.full_name, short_name=rate.short_name, exchange_rate=rate.exchange_rate)
        data.save()


def make_exchange(data):
    currency_from = data['currency_from']
    currency_to = data['currency_to']
    amount = data['amount']

    try:
        src_currency = CurrencyData.objects.get(short_name__exact=currency_from)
        dst_currency = CurrencyData.objects.get(short_name__exact=currency_to)

    except CurrencyData.DoesNotExist as e:
        # TODO: make it cleaner
        raise

    result = Decimal(amount) / src_currency.exchange_rate * dst_currency.exchange_rate

    # need to reformat this
    data = {amount + ' ' + currency_from: str(round(result, CURRENCY_PRECISION)) + ' ' + currency_to}

    return data
