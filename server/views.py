from django.shortcuts import render
import pandas as pd
from django.views import View
from .models import StockModel
from plotly.offline import plot
import plotly.graph_objs as go

def populate():
    df = pd.read_csv('./stock_market_data.csv')
    df['volume'] = df['volume'].str.replace(',', '').astype(int)
    df['high'] = df['high'].str.replace(',', '').astype(float)
    df['low'] = df['low'].str.replace(',', '').astype(float)
    df['open'] = df['open'].str.replace(',', '').astype(float)
    df['close'] = df['close'].str.replace(',', '').astype(float)
    
    i = 0
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
        i= i+1
        print("Stocks Saved", i)

class StockPopulate(View):
    def get(self, request):
        populate()
    return "Done"



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


class GraphView(View):
    def get(self, request):
        data = StockModel.objects.all()

        fig = go.Figure()

        x_values = list(data.values_list('date', flat=True))
        y_values_close = list(data.values_list('close', flat=True))
        y_values_volume = list(data.values_list('volume', flat=True))

        line_chart = go.Scatter(x=x_values, y=y_values_close, mode='lines', name='Close Price')
        bar_chart = go.Bar(x=x_values, y=y_values_volume, name='Volume', yaxis='y2')

        fig.add_trace(line_chart)
        fig.add_trace(bar_chart)

        fig.update_layout(
            title='Stock Data Visualization',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Close Price', side='left'),
            yaxis2=dict(title='Volume', overlaying='y', side='right'),
            legend=dict(x=0, y=1, traceorder='normal', orientation='h'),
        )

        dropdown_options = [code for code in data.values_list('trade_code', flat=True).distinct()]
        button_config = [
            {
                'args': [
                    {'y': [list(data.filter(trade_code=code).values_list('close', flat=True))]},
                    {'yaxis': {'title': 'Close Price'}}
                ],
                'label': code,
                'method': 'relayout',
            } for code in dropdown_options
        ]

        fig.update_layout(
            updatemenus=[
                {
                    'buttons': button_config,
                    'direction': 'down',
                    'showactive': True,
                    'x': 0.1,
                    'xanchor': 'left',
                    'y': 1.15,
                    'yanchor': 'top',
                },
            ],
        )

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        return render(request, 'chart.html', context={'plot_div': plot_div, 'plot_script': plot_div})