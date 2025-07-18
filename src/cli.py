import argparse
import logging
import logging.config
import os
import sys
from .data_fetcher import fetch_stock_data
from .parametric_var import calculate_parametric_var
from .historical_var import calculate_historical_var
from .monte_carlo_var import calculate_monte_carlo_var
from .report_generator import save_portfolio_data, generate_comparison_plot
from config import settings

# Setup logging
try:
    logging.config.fileConfig(
        settings.LOGGING_CONF,
        defaults={'logfilename': os.path.join(settings.LOGS_DIR, 'app.log')}
    )
except FileNotFoundError:
    # Fallback basic configuration if logging.conf is missing
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(os.path.join(settings.LOGS_DIR, 'app.log'))
        ]
    )
    
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description='Calculate Value at Risk (VaR) for Indian stocks using three methodologies',
        epilog='Example: python main.py RELIANCE NSE 1000000 --confidence 0.99 --horizon 5'
    )
    
    # Required arguments
    parser.add_argument(
        'ticker', 
        type=str, 
        help='Stock ticker symbol (e.g.: RELIANCE, INFY)'
    )
    parser.add_argument(
        'exchange', 
        type=str, 
        choices=['NSE', 'BSE'],
        help='Stock exchange: NSE or BSE'
    )
    parser.add_argument(
        'portfolio_value', 
        type=float, 
        help='Portfolio value in INR (e.g.: 1000000)'
    )
    
    # Optional parameters
    parser.add_argument(
        '--confidence', 
        type=float, 
        default=0.95,
        choices=[0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99],
        help='Confidence level (0.90-0.99) [default: 0.95]'
    )
    parser.add_argument(
        '--horizon', 
        type=int, 
        default=1,
        help='Time horizon in days [default: 1]'
    )
    parser.add_argument(
        '--window', 
        type=int, 
        default=252,
        help='Historical data window size in days [default: 252]'
    )
    parser.add_argument(
        '--simulations', 
        type=int, 
        default=10000,
        help='Monte Carlo simulations count [default: 10000]'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate inputs
        if not 0.90 <= args.confidence <= 0.99:
            raise ValueError("Confidence level must be between 0.90 and 0.99")
        if args.portfolio_value <= 0:
            raise ValueError("Portfolio value must be positive")
        if args.horizon <= 0:
            raise ValueError("Time horizon must be positive")
        if args.window <= 0:
            raise ValueError("Data window size must be positive")
        if args.simulations <= 0:
            raise ValueError("Simulation count must be positive")
            
        logger.info(f"Calculating VaR for {args.ticker} on {args.exchange}")
        logger.info(f"Portfolio value: ₹{args.portfolio_value:,.2f}")
        logger.info(f"Confidence: {args.confidence*100}%, Horizon: {args.horizon} days")
        logger.info(f"Data window: {args.window} days, Simulations: {args.simulations}")
        
        # Fetch stock data
        returns = fetch_stock_data(
            args.ticker, 
            args.exchange, 
            args.window
        )
        
        # Calculate VaR using different methods
        parametric_var = calculate_parametric_var(
            returns, 
            args.portfolio_value, 
            args.confidence, 
            args.horizon
        )
        
        historical_var = calculate_historical_var(
            returns, 
            args.portfolio_value, 
            args.confidence, 
            args.horizon
        )
        
        monte_carlo_var = calculate_monte_carlo_var(
            returns, 
            args.portfolio_value, 
            args.confidence, 
            args.horizon, 
            args.simulations
        )
        
        # Save portfolio data
        portfolio_file = save_portfolio_data(
            args.ticker,
            args.exchange,
            args.portfolio_value
        )
        
        # Generate report
        plot_file = generate_comparison_plot(
            parametric_var,
            historical_var,
            monte_carlo_var,
            args.portfolio_value,
            args.ticker,
            args.exchange
        )
        
        # Print results
        print(f"\nValue at Risk for {args.ticker} ({args.exchange}) portfolio of value ₹{args.portfolio_value:,.2f}:")
        print(f"• Parametric VaR:   ₹{parametric_var:,.2f}")
        print(f"• Historical VaR:   ₹{historical_var:,.2f}")
        print(f"• Monte Carlo VaR:  ₹{monte_carlo_var:,.2f}")
        print(f"\nPortfolio data saved as: '{os.path.basename(portfolio_file)}'")
        print(f"Comparison plot saved as: '{os.path.basename(plot_file)}'")
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        print(f"\nError: {str(e)}")
        print("Please check the logs for more details.")
        sys.exit(1)

if __name__ == '__main__':
    main()
