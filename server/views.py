from django.shortcuts import render

# Create your views here.

class StockJSONView(View):
    json = '/stock_market_data.csv'
    print(json)