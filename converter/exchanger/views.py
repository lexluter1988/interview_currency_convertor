# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


from forms import CurrencyForm
from messages import ApiMessages
from models import CurrencyData
from oexchangerateconnector import OpenExchangeRateConnector
from serializers import CurrencyDataSerializer, InputSerializer


def index(request):
    form = CurrencyForm()
    context = {'form': form}
    return render(request, 'exchanger/index.html', context)


@api_view(['GET'])
def currency_rate_list(request):
    """
    Getting all Currencies with rates and latest update time.
    """
    if request.method == 'GET':
        check_rates()
        rates = CurrencyData.objects.all()
        serializer = CurrencyDataSerializer(rates, many=True)
        return Response(serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def currency_rate_detail(request, pk):
    check_rates()
    try:
        currency = CurrencyData.objects.get(pk=pk)
    except CurrencyData.DoesNotExist:
        return Response(data=ApiMessages.CURRENCY_NO_INFO, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CurrencyDataSerializer(currency)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def currency_convert(request):
    check_rates()
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InputSerializer(data=data)
        if serializer.is_valid():
            try:
                src_currency = CurrencyData.objects.get(short_name__exact=data['currency_from'])
                dst_currency = CurrencyData.objects.get(short_name__exact=data['currency_to'])
                amount = data['amount']

                result = make_exchange(src_currency, dst_currency, amount)

            except CurrencyData.DoesNotExist:
                return Response(data=ApiMessages.CURRENCY_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

            return Response(result)

        return Response(data=ApiMessages.INVALID_REQUEST_AMOUNT, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def check_rates():
    # if no data about exchange rates, let's fill the DB
    if not CurrencyData.objects.exists():
        update_rates()
    # if rates are outdated more than 1 day, let's update them
    elif (timezone.now() - CurrencyData.objects.last().updated).days >= settings.DAYS_OF_INACTIVITY:
        CurrencyData.objects.all().delete()
        update_rates()


def update_rates():
    client = OpenExchangeRateConnector(settings.OPEN_EXCHANGE_RATES_API_KEY)
    rates = client.get_all_rates()
    for rate in rates:
        data = CurrencyData(full_name=rate.full_name, short_name=rate.short_name, exchange_rate=rate.exchange_rate)
        data.save()


def make_exchange(src_currency, dst_currency, amount):
    result = Decimal(amount) / src_currency.exchange_rate * dst_currency.exchange_rate
    return str(round(result, settings.CURRENCY_PRECISION))