from django.shortcuts import render
import pandas as pd
from django.views import View



#This Class Is to View JSON Data

class StockJSONView(View):
    df = None

    def get(self, request):

        print("Requesting JSON Data")

        if self.df is None:
            self.df = pd.read_json('./stock_market_data.json')
        print(self.df)
        return render(request, 'index.html', {'stocks': self.df.to_dict(orient='records')})