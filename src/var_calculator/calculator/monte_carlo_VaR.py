import numpy as np
from scipy.stats import norm

def calculate_monte_carlo_VaR(returns, portfolio_value, confidence_level=0.95, horizon=1, simulations=10000):
    """
    Calculate Value at Risk using Monte Carlo simulation.
    
    :param returns: Array of historical returns
    :param portfolio_value: Current portfolio value
    :param confidence_level: Confidence level (0.90-0.99)
    :param horizon: Time horizon in days
    :param simulations: Number of simulations
    :return: Monte Carlo VaR value
    """
    mean = np.mean(returns)
    std = np.std(returns)
    
    # Simulate future returns
    simulated_returns = np.random.normal(mean, std, (simulations, horizon))
    portfolio_paths = portfolio_value * (1 + simulated_returns).cumprod(axis=1)
    
    # Calculate final portfolio values
    final_values = portfolio_paths[:, -1]
    losses = portfolio_value - final_values
    
    # Calculate VaR
    VaR = np.percentile(losses, 100 * confidence_level)
    return max(0, VaR)
