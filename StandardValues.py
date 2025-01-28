import yfinance as yf
import numpy as np

def calculate_average_return_and_volatility(stock_symbol, start_date, end_date):
    
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    
    daily_returns = stock_data['Adj Close'].pct_change().dropna()

    
    average_return = daily_returns.mean() 

    
    volatility = daily_returns.std() 

    return average_return, volatility


stock_symbol = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-01-01'

average_return, volatility = calculate_average_return_and_volatility(stock_symbol, start_date, end_date)
print(f"Asset: {stock_symbol}")
print(f"Average Return: {average_return}")
print(f"Volatility: {volatility}")
