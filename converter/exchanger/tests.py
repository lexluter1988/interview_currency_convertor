# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .models import CurrencyData

# python manage.py test exchanger.tests


class BaseCurrencyDataTest(TestCase):
    """ Test module for CurrencyData model """

    def setUp(self):
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



