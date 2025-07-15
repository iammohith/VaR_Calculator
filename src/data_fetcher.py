import yfinance as yf
import pandas as pd
import numpy as np
import logging
from .exceptions import DataFetchError

logger = logging.getLogger(__name__)

def fetch_stock_data(ticker, exchange, window=252):
    """
    Fetch historical stock data from Yahoo Finance API.
    
    :param ticker: Stock ticker symbol
    :param exchange: Stock exchange (NSE or BSE)
    :param window: Historical data window size (days)
    :return: Array of daily returns
    """
    try:
        # Validate exchange
        exchange = exchange.upper()
        if exchange not in ['NSE', 'BSE']:
            raise ValueError("Invalid exchange. Use 'NSE' or 'BSE'")
        
        # Format ticker for Yahoo Finance
        symbol = f"{ticker}.{'NS' if exchange == 'NSE' else 'BO'}"
        logger.info(f"Fetching {window} days of data for {symbol}")
        
        # Fetch historical data
        stock = yf.Ticker(symbol)
        hist = stock.history(period=f"{window}d")
        
        if hist.empty:
            raise DataFetchError(f"No data found for {symbol}")
        
        # Calculate daily log returns (more stable for financial calculations)
        close_prices = hist['Close']
        returns = np.log(close_prices / close_prices.shift(1)).dropna().values
        
        if len(returns) < window * 0.9:  # Allow 10% missing data
            raise DataFetchError("Insufficient data for accurate calculation")
            
        logger.info(f"Successfully fetched {len(returns)} days of returns data")
        return returns
        
    except Exception as e:
        logger.error(f"Data fetch error: {str(e)}")
        raise DataFetchError(f"Failed to fetch data: {str(e)}")
