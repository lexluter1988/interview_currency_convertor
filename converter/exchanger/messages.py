#!/usr/bin/python
# -*- coding: utf-8 -*-


class ApiMessages:
    def __init__(self):
        pass

    CURRENCY_NOT_FOUND = {"error code": 404, "error message": "There is no such currency or you mistyped it"}
    CURRENCY_NO_INFO = {"error code": 404, "error message": "Application doesn't have this currency rates"}
    INVALID_REQUEST_AMOUNT = {"error code": 204, "error message": "Wrong amount in request, it should be numeric"}
