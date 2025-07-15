import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def fetch_stock_data(ticker: str, exchange: str, window: int) -> pd.Series:
    """
    Fetch historical stock data from Yahoo Finance
    """
    # Add exchange suffix
    if exchange == "NSE":
        symbol = f"{ticker}.NS"
    elif exchange == "BSE":
        symbol = f"{ticker}.BO"
    else:
        raise ValueError(f"Unsupported exchange: {exchange}")
    
    logger.info(f"Fetching data for {symbol}")
    stock = yf.Ticker(symbol)
    data = stock.history(period=f"{window}d")
    
    if data.empty:
        raise ValueError(f"No data found for {symbol}")
    
    # Calculate daily returns
    returns = data['Close'].pct_change().dropna()
    return returns
