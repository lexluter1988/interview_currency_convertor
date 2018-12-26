#!/bin/bash

virtualenv -p /usr/bin/python ./env
. env/bin/activate
pip install -r requirements.txt
cd converter
python manage.py test exchanger.tests -v 3
python manage.py migrate
python manage.py runserver