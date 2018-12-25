# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
import json
from django.urls import reverse
from rest_framework import status

from ..models import CurrencyData
from ..serializers import CurrencyDataSerializer
from ..messages import ApiMessages
from ..config import OPEN_EXCHANGE_RATES_API_KEY
from ..oexchangerateconnector import OpenExchangeRateConnector

client = Client()


class BaseCurrencyDataTest(TestCase):
    """ Test module for CurrencyData model """

    def setUp(self):
        self.valid_payload = {
            'currency_from': 'CZK',
            'currency_to': "EUR",
            'amount': '10000'
        }
        self.invalid_amount = {
            'currency_from': 'CZK',
            'currency_to': "EUR",
            'amount': 'xxx'
        }

        self.invalid_currency = {
            'currency_from': '111',
            'currency_to': "1111",
            'amount': '1000'
        }

        self.invalid_json = {
            'invalid': 'data'
        }

        CurrencyData.objects.create(
            full_name='Czech Republic Koruna', short_name='CZK', exchange_rate=22.6887920000)
        CurrencyData.objects.create(
            full_name='Euro', short_name='EUR', exchange_rate=0.8770150000)
        CurrencyData.objects.create(
            full_name='Polish Zloty', short_name='PLN', exchange_rate=3.7598500000)
        CurrencyData.objects.create(
            full_name='United States Dollar', short_name='USD', exchange_rate=1)

    def test_currencies_created(self):

        czk = CurrencyData.objects.get(full_name='Czech Republic Koruna')
        eur = CurrencyData.objects.get(full_name='Euro')
        pln = CurrencyData.objects.get(full_name='Polish Zloty')
        usd = CurrencyData.objects.get(full_name='United States Dollar')

        self.assertEqual(
            czk.short_name, 'CZK')
        self.assertEqual(
            eur.short_name, 'EUR')
        self.assertEqual(
            pln.short_name, 'PLN')
        self.assertEqual(
            usd.exchange_rate, 1)

    def test_get_all_currencies(self):
        response = client.get(reverse('currency_rate_list'))

        currencies = CurrencyData.objects.all()
        serializer = CurrencyDataSerializer(currencies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_first_currency(self):
        response = client.get(reverse('currency_rate_detail', kwargs={'pk': 1}))

        currency = CurrencyData.objects.get(pk=1)
        serializer = CurrencyDataSerializer(currency, many=False)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_convert_valid_currency(self):
        answer = '386.54107'
        response = client.post(
            reverse('currency_convert'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, answer)

    def test_convert_invalid_amount(self):
        response = client.post(
            reverse('currency_convert'),
            data=json.dumps(self.invalid_amount),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, ApiMessages.INVALID_REQUEST_AMOUNT)

    def test_convert_invalid_currency(self):
        response = client.post(
            reverse('currency_convert'),
            data=json.dumps(self.invalid_currency),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, ApiMessages.CURRENCY_NOT_FOUND)

    def test_convert_invalid_request_type(self):
        response = client.get(reverse('currency_convert'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_convert_invalid_json(self):
        response = client.post(
            reverse('currency_convert'),
            data=json.dumps(self.invalid_json),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class OpenExchangeRateConnectorTest(TestCase):
    """ Test module for ExchangeRateConnectorTest"""
    def test_get_all_rates(self):
        client = OpenExchangeRateConnector(OPEN_EXCHANGE_RATES_API_KEY)
        rates = client.get_all_rates()
        self.assert_(len(rates) > 0)



