import numpy as np
import logging

logger = logging.getLogger(__name__)

def calculate_historical_var(returns, portfolio_value, confidence_level=0.95, horizon=1):
    """
    Calculate Value at Risk using historical simulation method.
    
    :param returns: Array of historical log returns
    :param portfolio_value: Current portfolio value
    :param confidence_level: Confidence level (0.90-0.99)
    :param horizon: Time horizon in days
    :return: Historical VaR value
    """
    try:
        # Simulate horizon-day returns by summing random horizon periods
        horizon_returns = []
        for _ in range(10000):  # Use 10,000 random samples
            random_indices = np.random.choice(len(returns), horizon, replace=True)
            cumulative_return = np.sum(returns[random_indices])
            horizon_returns.append(cumulative_return)
        
        # Calculate portfolio values after horizon
        portfolio_values = portfolio_value * np.exp(horizon_returns)
        
        # Calculate VaR as the loss at the confidence level
        sorted_values = np.sort(portfolio_values)
        index = int((1 - confidence_level) * len(sorted_values))
        var = portfolio_value - sorted_values[index]
        
        logger.info(f"Historical VaR calculated: ₹{var:,.2f} at {confidence_level*100}% confidence")
        return max(0, var)  # Ensure non-negative value
        
    except Exception as e:
        logger.error(f"Historical VaR calculation error: {str(e)}")
        raise
