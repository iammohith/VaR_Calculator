import numpy as np
import pandas as pd
from scipy.stats import norm

def calculate_monte_carlo_var(returns: pd.Series, portfolio_value: float, 
                             confidence: float, horizon: int, simulations: int) -> float:
    """
    Calculate VaR using Monte Carlo simulation
    """
    mean = returns.mean()
    std = returns.std()
    
    # Generate random returns
    simulated_returns = np.random.normal(mean, std, simulations)
    
    # Calculate portfolio values
    portfolio_values = portfolio_value * (1 + simulated_returns)
    
    # Sort and find VaR
    portfolio_values.sort()
    var_index = int((1 - confidence) * simulations)
    var = portfolio_value - portfolio_values[var_index]
    return var
