#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import CURRENCY_FILTER

from openexchangerates import OpenExchangeRatesClient


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

            if short_name not in CURRENCY_FILTER:
                continue

            full_name = currencies[currency]
            exchange_rate = latest[currency]

            rates.append(ExchangeRateData(short_name=short_name, full_name=full_name, exchange_rate=exchange_rate))
        return rates


