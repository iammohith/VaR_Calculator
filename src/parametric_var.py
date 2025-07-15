import numpy as np
from scipy.stats import norm
import logging

logger = logging.getLogger(__name__)

def calculate_parametric_var(returns, portfolio_value, confidence_level=0.95, horizon=1):
    """
    Calculate Value at Risk using parametric (variance-covariance) method.
    
    :param returns: Array of historical log returns
    :param portfolio_value: Current portfolio value
    :param confidence_level: Confidence level (0.90-0.99)
    :param horizon: Time horizon in days
    :return: Parametric VaR value
    """
    try:
        # Calculate mean and standard deviation of returns
        mean = np.mean(returns)
        std = np.std(returns)
        
        # Calculate z-score based on confidence level
        z_score = norm.ppf(1 - confidence_level)
        
        # Calculate VaR - using log returns properties
        var = portfolio_value * (1 - np.exp(mean * horizon - z_score * std * np.sqrt(horizon)))
        
        logger.info(f"Parametric VaR calculated: ₹{var:,.2f} at {confidence_level*100}% confidence")
        return var
        
    except Exception as e:
        logger.error(f"Parametric VaR calculation error: {str(e)}")
        raise
