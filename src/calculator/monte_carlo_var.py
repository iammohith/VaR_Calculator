import numpy as np
from scipy.stats import norm
from ..core.exceptions import InvalidConfidenceLevel

def calculate_monte_carlo_var(returns: np.ndarray, portfolio_value: float, 
                            confidence_level: float = 0.95, 
                            simulations: int = 10000) -> float:
    """
    Calculate VaR using Monte Carlo simulation
    """
    if not 0.90 <= confidence_level <= 0.99:
        raise InvalidConfidenceLevel("Confidence level must be between 0.90 and 0.99")
    
    mean = np.mean(returns)
    std_dev = np.std(returns)
    
    # Generate simulated returns
    simulated_returns = np.random.normal(mean, std_dev, simulations)
    
    # Sort the simulated returns
    simulated_returns_sorted = np.sort(simulated_returns)
    
    # Calculate VaR at the specified confidence level
    index = int((1 - confidence_level) * simulations)
    if index >= len(simulated_returns_sorted):
        index = len(simulated_returns_sorted) - 1
    
    var = portfolio_value * abs(simulated_returns_sorted[index])
    return var
