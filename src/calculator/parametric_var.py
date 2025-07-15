import numpy as np
from scipy.stats import norm

def calculate_parametric_var(returns: pd.Series, portfolio_value: float, 
                            confidence: float, horizon: int) -> float:
    """
    Calculate VaR using parametric (variance-covariance) method
    """
    mean = returns.mean()
    std = returns.std()
    
    # Calculate z-score based on confidence level
    z_score = norm.ppf(1 - confidence)
    
    # Calculate daily VaR
    daily_var = portfolio_value * (mean - z_score * std)
    
    # Adjust for horizon
    return daily_var * np.sqrt(horizon)
