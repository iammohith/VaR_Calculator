import argparse
import logging
import logging.config
import os
import numpy as np
from config import settings
from .core import data_fetcher, report_VaR
from .calculator import historical_VaR, monte_carlo_VaR, parametric_VaR

# Setup logging
logging.config.fileConfig(
    os.path.join(settings.BASE_DIR, 'config', 'logging.conf'),
    defaults={'logfilename': os.path.join(settings.LOGS_DIR, 'app.log')}
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Calculate Value at Risk (VaR) for Indian stocks.')
    parser.add_argument('ticker', type=str, help='Stock ticker symbol')
    parser.add_argument('exchange', type=str, help='Stock exchange (NSE or BSE)')
    parser.add_argument('portfolio_value', type=float, help='Portfolio value in INR')
    parser.add_argument('--confidence', type=float, default=0.95, help='Confidence level (0.90-0.99)')
    parser.add_argument('--horizon', type=int, default=1, help='Time horizon in days')
    parser.add_argument('--window', type=int, default=252, help='Historical data window size')
    parser.add_argument('--simulations', type=int, default=10000, help='Monte Carlo simulations count')
    
    args = parser.parse_args()
    
    try:
        # Validate confidence level
        if not 0.90 <= args.confidence <= 0.99:
            raise ValueError("Confidence level must be between 0.90 and 0.99")
            
        logger.info(f"Calculating VaR for {args.ticker} on {args.exchange}")
        logger.info(f"Portfolio value: ₹{args.portfolio_value:,.2f}")
        logger.info(f"Confidence: {args.confidence*100}%, Horizon: {args.horizon} days")
        
        # Fetch stock data
        returns = data_fetcher.fetch_stock_data(
            args.ticker, 
            args.exchange, 
            args.window
        )
        
        # Calculate VaR using different methods
        parametric_var = parametric_VaR.calculate_parametric_VaR(
            returns, 
            args.portfolio_value, 
            args.confidence, 
            args.horizon
        )
        
        historical_var = historical_VaR.calculate_historical_VaR(
            returns, 
            args.portfolio_value, 
            args.confidence, 
            args.horizon
        )
        
        monte_carlo_var = monte_carlo_VaR.calculate_monte_carlo_VaR(
            returns, 
            args.portfolio_value, 
            args.confidence, 
            args.horizon, 
            args.simulations
        )
        
        # Save portfolio data
        portfolio_file = report_VaR.save_portfolio_data(
            args.ticker,
            args.exchange,
            args.portfolio_value,
            settings.CURRENT_USER,
            settings.TIMESTAMP
        )
        
        # Generate report
        plot_file = report_VaR.generate_comparison_plot(
            parametric_var,
            historical_var,
            monte_carlo_var,
            args.portfolio_value,
            args.ticker,
            settings.CURRENT_USER,
            settings.TIMESTAMP
        )
        
        # Print results
        print(f"\nValue at Risk for {args.ticker} portfolio of value ₹{args.portfolio_value:,.2f}:")
        print(f"Parametric VaR: ₹{parametric_var:,.2f}")
        print(f"Historical VaR: ₹{historical_var:,.2f}")
        print(f"Monte Carlo VaR: ₹{monte_carlo_var:,.2f}")
        print(f"\nPortfolio data saved as: '{os.path.basename(portfolio_file)}'")
        print(f"Comparison plot saved as '{os.path.basename(plot_file)}'")
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
