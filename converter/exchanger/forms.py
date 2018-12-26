#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms


class CurrencyForm(forms.Form):
    amount = forms.CharField(label='Amount to be converted', max_length=100)