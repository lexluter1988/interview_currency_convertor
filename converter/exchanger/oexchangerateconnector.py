#!/usr/bin/python
# -*- coding: utf-8 -*-
from openexchangerates import OpenExchangeRatesClient



# write filter to set only Check Coruna, Euro, Polish Zlot and US
# decorator for get_all_rates will be good


class ExchangeRateData:
    def __init__(self, short_name, full_name, exchange_rate):
        self.short_name = short_name
        self.full_name = full_name
        self.exchange_rate = exchange_rate


class OpenExchangeRateConnector:
    def __init__(self, api_key):
        self.client = OpenExchangeRatesClient(api_key)

    def get_all_rates(self):
        currencies = self.client.currencies()
        latest = self.client.latest()['rates']

        rates = []

        for currency in currencies:

            short_name = currency
            full_name = currencies[currency]
            exchange_rate = latest[currency]

            rates.append(ExchangeRateData(short_name=short_name, full_name=full_name, exchange_rate=exchange_rate))
        return rates


