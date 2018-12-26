#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from config import CURRENCY_FILTER, CURRENCY_PRECISION


class CurrencyForm(forms.Form):
    source_currency = forms.ChoiceField(label='Currency From', choices=enumerate(tuple(CURRENCY_FILTER)), required=True)
    amount = forms.DecimalField(label='Amount to be converted', max_digits=20, decimal_places=CURRENCY_PRECISION)
    destination_currency = forms.ChoiceField(label='Currency To', choices=enumerate(tuple(CURRENCY_FILTER)), required=True)
    result = forms.DecimalField(label='Result will be displayed here', max_digits=20, decimal_places=CURRENCY_PRECISION, required=False)
