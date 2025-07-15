import argparse
import logging
import logging.config
import os
from config import settings
from src.core import data_fetcher, exceptions, risk_report
from src.calculator import (
    historical_var, 
    monte_carlo_var, 
    parametric_var
)

# Setup logging
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'logging.conf')
logging.config.fileConfig(config_path)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Calculate Value at Risk for Indian stocks')
    
    # Required arguments
    parser.add_argument('ticker', help='Stock ticker symbol')
    parser.add_argument('exchange', choices=['NSE', 'BSE'], help='Stock exchange')
    parser.add_argument('portfolio_value', type=float, help='Portfolio value in INR')
    
    # Optional parameters
    parser.add_argument('--confidence', type=float, default=settings.DEFAULT_CONFIDENCE,
                        help='Confidence level (0.90-0.99)')
    parser.add_argument('--horizon', type=int, default=settings.DEFAULT_HORIZON,
                        help='Time horizon in days')
    parser.add_argument('--window', type=int, default=settings.DEFAULT_WINDOW,
                        help='Historical data window size (days)')
    parser.add_argument('--simulations', type=int, default=settings.DEFAULT_SIMULATIONS,
                        help='Monte Carlo simulations count')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not 0.90 <= args.confidence <= 0.99:
        raise exceptions.InvalidInputError("Confidence level must be between 0.90 and 0.99")
    
    try:
        # Fetch data
        returns = data_fetcher.fetch_stock_data(
            args.ticker, 
            args.exchange, 
            args.window
        )
        
        # Calculate VaR using different methods
        results = {}
        
        # Parametric VaR
        results['Parametric'] = parametric_var.calculate_parametric_var(
            returns,
            args.portfolio_value,
            args.confidence,
            args.horizon
        )
        
        # Historical VaR
        results['Historical'] = historical_var.calculate_historical_var(
            returns,
            args.portfolio_value,
            args.confidence
        )
        
        # Monte Carlo VaR
        results['Monte Carlo'] = monte_carlo_var.calculate_monte_carlo_var(
            returns,
            args.portfolio_value,
            args.confidence,
            args.horizon,
            args.simulations
        )
        
        # Generate report
        report = risk_report.generate_report(results, args.portfolio_value)
        print(report)
        
    except Exception as e:
        logger.error(f"Error calculating VaR: {str(e)}")
        raise

if __name__ == "__main__":
    main()
