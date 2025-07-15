import argparse
import logging
import logging.config
import os
import numpy as np
import pandas as pd
from core.data_fetcher import fetch_stock_data
from core.risk_report import generate_report
from calculator.parametric_var import calculate_parametric_var
from calculator.historical_var import calculate_historical_var
from calculator.monte_carlo_var import calculate_monte_carlo_var
from core.exceptions import DataFetchError, InvalidConfidenceLevel
from config import settings

# Setup logging
log_config_path = os.path.join(os.path.dirname(__file__), '../config/logging.conf')
if os.path.exists(log_config_path):
    logging.config.fileConfig(log_config_path)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Value at Risk Calculator for Indian Stocks')
    
    # Required arguments
    parser.add_argument('ticker', type=str, help='Stock ticker symbol')
    parser.add_argument('exchange', type=str, choices=['NSE', 'BSE'], help='Stock exchange (NSE or BSE)')
    parser.add_argument('portfolio_value', type=float, help='Portfolio value in INR')
    
    # Optional parameters
    parser.add_argument('--confidence', type=float, default=settings.DEFAULTS['confidence_level'],
                       help='Confidence level (0.90-0.99)')
    parser.add_argument('--horizon', type=int, default=settings.DEFAULTS['time_horizon'],
                       help='Time horizon in days')
    parser.add_argument('--window', type=int, default=settings.DEFAULTS['window_size'],
                       help='Historical data window size (days)')
    parser.add_argument('--simulations', type=int, default=settings.DEFAULTS['monte_carlo_simulations'],
                       help='Monte Carlo simulations count')
    
    args = parser.parse_args()
    
    try:
        # Validate confidence level
        if not 0.90 <= args.confidence <= 0.99:
            raise InvalidConfidenceLevel("Confidence level must be between 0.90 and 0.99")
        
        # Fetch stock data
        logger.info(f"Fetching data for {args.ticker} from {args.exchange}")
        data = fetch_stock_data(args.ticker, args.exchange, period=f'{args.window}d')
        
        # Calculate daily returns
        returns = np.log(data / data.shift(1)).dropna()
        
        # Adjust returns for time horizon
        horizon_adjusted_returns = returns * np.sqrt(args.horizon)
        
        # Calculate VaR using different methods
        parametric_var = calculate_parametric_var(
            horizon_adjusted_returns, args.portfolio_value, args.confidence
        )
        
        historical_var = calculate_historical_var(
            horizon_adjusted_returns, args.portfolio_value, args.confidence
        )
        
        monte_carlo_var = calculate_monte_carlo_var(
            horizon_adjusted_returns, args.portfolio_value, 
            args.confidence, args.simulations
        )
        
        # Generate report
        results = {
            "Parametric": parametric_var,
            "Historical": historical_var,
            "Monte Carlo": monte_carlo_var
        }
        
        report = generate_report(results, args.portfolio_value)
        print(report)
        
    except (DataFetchError, InvalidConfidenceLevel, ValueError) as e:
        logger.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}")
        exit(1)
    except Exception as e:
        logger.exception("Unexpected error occurred")
        print(f"Unexpected error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
