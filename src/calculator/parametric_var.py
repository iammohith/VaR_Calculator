import numpy as np
from scipy.stats import norm
from ..core.exceptions import InvalidConfidenceLevel

def calculate_parametric_var(returns: np.ndarray, portfolio_value: float, 
                            confidence_level: float = 0.95) -> float:
    """
    Calculate VaR using parametric method
    """
    if not 0.90 <= confidence_level <= 0.99:
        raise InvalidConfidenceLevel("Confidence level must be between 0.90 and 0.99")
    
    mean = np.mean(returns)
    std_dev = np.std(returns)
    z_score = norm.ppf(1 - confidence_level)
    
    var = portfolio_value * (mean - z_score * std_dev)
    return abs(var)
