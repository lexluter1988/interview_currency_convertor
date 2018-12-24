#!/usr/bin/python
# -*- coding: utf-8 -*-
from openexchangerates import OpenExchangeRatesClient
from convertor.exchange_rest_service.config import OPEN_EXCHANGE_RATES_API_KEY
from pprint import pprint

client = OpenExchangeRatesClient(OPEN_EXCHANGE_RATES_API_KEY)
currencies = client.currencies()
latest = client.latest()

pprint(currencies)
pprint(latest)

