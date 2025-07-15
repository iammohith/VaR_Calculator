import yfinance as yf
import pandas as pd
from .exceptions import DataFetchError

def fetch_stock_data(ticker: str, exchange: str, period: str = '1y') -> pd.Series:
    """
    Fetch historical stock data
    """
    try:
        # Handle exchange-specific ticker formatting
        if exchange == 'BSE':
            ticker += '.BO'
        elif exchange == 'NSE':
            ticker += '.NS'
        
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)['Close']
        if data.empty:
            raise DataFetchError(f"No data found for {ticker} on {exchange}")
        return data
    except Exception as e:
        raise DataFetchError(f"Error fetching data: {str(e)}")
