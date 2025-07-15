import numpy as np
from scipy.stats import norm
import logging

logger = logging.getLogger(__name__)

def calculate_monte_carlo_var(returns, portfolio_value, confidence_level=0.95, horizon=1, simulations=10000):
    """
    Calculate Value at Risk using Monte Carlo simulation.
    
    :param returns: Array of historical log returns
    :param portfolio_value: Current portfolio value
    :param confidence_level: Confidence level (0.90-0.99)
    :param horizon: Time horizon in days
    :param simulations: Number of simulations
    :return: Monte Carlo VaR value
    """
    try:
        # Estimate parameters from historical returns
        mean = np.mean(returns)
        std = np.std(returns)
        
        # Simulate future returns
        daily_returns = np.random.normal(mean, std, (simulations, horizon))
        cumulative_returns = np.sum(daily_returns, axis=1)
        portfolio_values = portfolio_value * np.exp(cumulative_returns)
        
        # Calculate losses
        losses = portfolio_value - portfolio_values
        var = np.percentile(losses, 100 * confidence_level)
        
        logger.info(f"Monte Carlo VaR calculated: ₹{var:,.2f} at {confidence_level*100}% confidence")
        return max(0, var)  # Ensure non-negative value
        
    except Exception as e:
        logger.error(f"Monte Carlo VaR calculation error: {str(e)}")
        raise
