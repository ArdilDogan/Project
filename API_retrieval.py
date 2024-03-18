import requests
import concurrent.futures
from datetime import datetime, timedelta
from .API_retrieval import StockData

api_key = '4SPMlfBRZk9i_MUIj8aBjnwKv5WcwYD_'
tickers = ['AAPL', 'MSFT', 'GOOGL']


end_date = datetime.now()
start_date = end_date - timedelta(days=90)

start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

stock_data_objects = []

def fetch_and_create_stock_data(ticker):
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date_str}/{end_date_str}?adjusted=true&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return StockData(ticker, data)
    else:
        return None

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(fetch_and_create_stock_data, ticker) for ticker in tickers]
    
    for future in concurrent.futures.as_completed(futures):
        ticker, data = future.result()
        stock_data = future.result()
        if stock_data:
            stock_data_objects.append(stock_data)

