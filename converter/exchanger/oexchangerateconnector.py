#!/usr/bin/python
# -*- coding: utf-8 -*-
from openexchangerates import OpenExchangeRatesClient
from config import OPEN_EXCHANGE_RATES_API_KEY


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


# def dummy_test():
#     client = OpenExchangeRateConnector(OPEN_EXCHANGE_RATES_API_KEY)
#     r = client.get_all_rates()
#
#     for i in r:
#         print i.short_name, '-->', i.full_name, '-->', i.exchange_rate
#
#
# dummy_test()

