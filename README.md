Write a REST web service for currency conversion.
Exchange rates might be taken from free sources (e.g. https://openexchangerates.org/) and should be updated once a day.
User interface design is up to you. 
Currencies: Czech koruna, Euro, Polish złoty and US dollar.
The application should be tested as well. Code coverage is important.
The project should be uploaded to GitHub/Bitbucket.  


Usage:

* First, clone repo
   
 ```commandline
$ git clone https://github.com/lexluter1988/currency_convertor.git
```

* Go to the currency_convertor folder

 ```commandline
$ cd currency_convertor
```

* Run one-click installer
 ```commandline
$ chmod a+x installer.sh
$ ./install.sh
```

* The UI and REST API is ready to use
 ```commandline
Starting development server at http://127.0.0.1:8000/

```

* REST API example
 ```commandline
$ curl -X POST --data '{"currency_from":"CZK", "currency_to": "EUR", "amount":"10000"}' -H 'Content-Type: application/json' 'http://127.0.0.1:8000/convert/'

"386.29477"

```

* Configuration for supported currencies is inside converter/setting.py
 ```commandline
 # API KEY to https://openexchangerates.org/
OPEN_EXCHANGE_RATES_API_KEY= '53a064e1bf4e4187b2caa4404415c8a7'

# Filter for currencies you'd like to support for conversion
CURRENCY_FILTER = ['CZK', 'EUR', 'USD', 'PLN']

# Period of currencies exchange rate update
DAYS_OF_INACTIVITY = 1

# Precision of returned exchange
CURRENCY_PRECISION = 5
```
