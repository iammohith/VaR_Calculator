import numpy as np
from scipy.stats import norm

def calculate_parametric_VaR(returns, portfolio_value, confidence_level=0.95, horizon=1):
    """
    Calculate Value at Risk using parametric (variance-covariance) method.
    
    :param returns: Array of historical returns
    :param portfolio_value: Current portfolio value
    :param confidence_level: Confidence level (0.90-0.99)
    :param horizon: Time horizon in days
    :return: Parametric VaR value
    """
    mean = np.mean(returns)
    std = np.std(returns)
    
    # Calculate z-score based on confidence level
    z_score = norm.ppf(1 - confidence_level)
    
    # Calculate VaR
    VaR = portfolio_value * (z_score * std * np.sqrt(horizon) - mean * horizon)
    return abs(VaR)
