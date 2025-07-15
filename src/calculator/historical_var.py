import numpy as np
from ..core.exceptions import InvalidConfidenceLevel

def calculate_historical_var(returns: np.ndarray, portfolio_value: float, 
                            confidence_level: float = 0.95) -> float:
    """
    Calculate VaR using historical simulation
    """
    if not 0.90 <= confidence_level <= 0.99:
        raise InvalidConfidenceLevel("Confidence level must be between 0.90 and 0.99")
    
    # Calculate the percentile corresponding to the confidence level
    historical_returns_sorted = np.sort(returns)
    index = int((1 - confidence_level) * len(historical_returns_sorted))
    
    if index >= len(historical_returns_sorted):
        index = len(historical_returns_sorted) - 1
    
    var = portfolio_value * abs(historical_returns_sorted[index])
    return var
