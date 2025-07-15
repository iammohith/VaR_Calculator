import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from config import settings
except ImportError:
    print("Error importing settings")
    raise

logger = logging.getLogger(__name__)

def save_portfolio_data(ticker, exchange, portfolio_value, user, timestamp):
    """
    Save portfolio data to CSV file.
    
    :param ticker: Stock ticker
    :param exchange: Stock exchange
    :param portfolio_value: Portfolio value
    :param user: Current user
    :param timestamp: Timestamp
    :return: File path of saved data
    """
    try:
        data = {
            'ticker': [ticker],
            'exchange': [exchange],
            'portfolio_value': [portfolio_value],
            'user': [user],
            'timestamp': [timestamp]
        }
        df = pd.DataFrame(data)
        
        filename = f"portfolio_{user}_{ticker}_{timestamp}.csv"
        filepath = os.path.join(settings.PORTFOLIOS_DIR, filename)
        df.to_csv(filepath, index=False)
        
        logger.info(f"Portfolio data saved to {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error saving portfolio data: {str(e)}")
        raise

def generate_comparison_plot(parametric_var, historical_var, monte_carlo_var, 
                             portfolio_value, ticker, user, timestamp):
    """
    Generate comparison plot of VaR methodologies.
    
    :param parametric_var: Parametric VaR value
    :param historical_var: Historical VaR value
    :param monte_carlo_var: Monte Carlo VaR value
    :param portfolio_value: Portfolio value
    :param ticker: Stock ticker
    :param user: Current user
    :param timestamp: Timestamp
    :return: File path of saved plot
    """
    try:
        methods = ['Parametric', 'Historical', 'Monte Carlo']
        values = [parametric_var, historical_var, monte_carlo_var]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(methods, values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        
        plt.title(f'VaR Comparison for {ticker} (Portfolio Value: ₹{portfolio_value:,.2f})', fontsize=14)
        plt.xlabel('Methodology', fontsize=12)
        plt.ylabel('Value at Risk (₹)', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'₹{height:,.2f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom')
        
        # Save plot
        filename = f"var_report_{user}_{ticker}_{timestamp}.png"
        filepath = os.path.join(settings.REPORTS_DIR, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300)
        plt.close()
        
        logger.info(f"Comparison plot saved to {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error generating plot: {str(e)}")
        raise
