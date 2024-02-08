from django.shortcuts import render
import pandas as pd
from django.views import View
from .models import StockModel

def populate():
    df = pd.read_csv('./stock_market_data.csv')
    df['volume'] = df['volume'].str.replace(',', '').astype(int)
    df['high'] = df['high'].str.replace(',', '').astype(float)
    df['low'] = df['low'].str.replace(',', '').astype(float)
    df['open'] = df['open'].str.replace(',', '').astype(float)
    df['close'] = df['close'].str.replace(',', '').astype(float)
    

    for index, row in df.iterrows():
        stock = StockModel(
            date=row['date'],
            trade_code=row['trade_code'],
            high=row['high'],
            low=row['low'],
            open=row['open'],
            close=row['close'],
            volume=row['volume']
            )
        stock.save()
        print("Stocks Saved")


#This Class Is to View JSON Data

class StockJSONView(View):
    df = None

    def get(self, request):

        print("Requesting JSON Data")

        if self.df is None:
            self.df = pd.read_json('./stock_market_data.json')
        print(self.df)
        return render(request, 'index.html', {'stocks': self.df.to_dict(orient='records')})

class StockCSVView(View):
    def get(self, request):
        stock = StockModel.objects.all()
        print(stock)
        return render(request, 'database.html', {'stocks': stock})