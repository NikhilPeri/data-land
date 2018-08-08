import os
import requests
import pandas as pd

from StringIO import StringIO

ALPLA_VANTAGE_API = 'https://www.alphavantage.co/query'

def get_daily_prices(stock_symbol, full=False):
    params = {
        'symbol': stock_symbol,
        'outputsize': 'full' if full else 'compact',
        'apikey': os.environ['STOCK_API_KEY'],
        'datatype': 'csv',
        'function': 'TIME_SERIES_DAILY'
    }
    response = requests.get(ALPLA_VANTAGE_API, params=params)
    if response.ok:
        return pd.read_csv(StringIO(response.text))
    else:
        return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
