#!/usr/bin/python
# -*- coding: utf-8 -*-
from openexchangerates import OpenExchangeRatesClient
from converter.exchanger.config import OPEN_EXCHANGE_RATES_API_KEY

client = OpenExchangeRatesClient(OPEN_EXCHANGE_RATES_API_KEY)
currencies = client.currencies()
latest = client.latest()['rates']

for currency in currencies:
    print currency, '-->', currencies[currency], '-->', latest[currency]