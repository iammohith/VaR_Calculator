import yfinance as yf
import pandas as pd
import logging
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from .exceptions import DataFetchError
except ImportError:
    from src.var_calculator.core.exceptions import DataFetchError

logger = logging.getLogger(__name__)

def fetch_stock_data(ticker, exchange, window=252):
    """
    Fetch historical stock data from Yahoo Finance API.
    
    :param ticker: Stock ticker symbol
    :param exchange: Stock exchange (NSE or BSE)
    :param window: Historical data window size
    :return: Array of daily returns
    """
    try:
        # Format ticker based on exchange
        if exchange.upper() == 'NSE':
            symbol = f"{ticker}.NS"
        elif exchange.upper() == 'BSE':
            symbol = f"{ticker}.BO"
        else:
            raise ValueError("Invalid exchange. Use 'NSE' or 'BSE'")
        
        logger.info(f"Fetching data for {symbol}")
        stock = yf.Ticker(symbol)
        
        # Get historical market data
        hist = stock.history(period=f"{window}d")
        
        if hist.empty:
            raise DataFetchError(f"No data found for {symbol}")
        
        # Calculate daily returns
        returns = hist['Close'].pct_change().dropna().values
        
        if len(returns) < window * 0.9:  # Allow 10% missing data
            raise DataFetchError("Insufficient data for accurate calculation")
            
        return returns
        
    except Exception as e:
        logger.error(f"Data fetch error: {str(e)}")
        raise DataFetchError(f"Failed to fetch data: {str(e)}")
