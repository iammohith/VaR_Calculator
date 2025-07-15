import numpy as np

def calculate_historical_VaR(returns, portfolio_value, confidence_level=0.95, horizon=1):
    """
    Calculate Value at Risk using historical simulation method.
    
    :param returns: Array of historical returns
    :param portfolio_value: Current portfolio value
    :param confidence_level: Confidence level (0.90-0.99)
    :param horizon: Time horizon in days
    :return: Historical VaR value
    """
    # Adjust returns for time horizon
    horizon_returns = returns * np.sqrt(horizon)
    
    # Calculate the VaR
    VaR = np.percentile(horizon_returns, 100 * (1 - confidence_level))
    return abs(VaR) * portfolio_value
