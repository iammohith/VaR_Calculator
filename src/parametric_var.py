import numpy as np
from scipy.stats import norm
import logging

logger = logging.getLogger(__name__)

def calculate_parametric_var(returns, portfolio_value, confidence_level=0.95, horizon=1):
    """
    Calculate Value at Risk using parametric (variance-covariance) method.
    
    Industry Standards:
    - Uses log returns for better financial modeling
    - Properly scales volatility with square root of time
    - Represents loss as positive value
    - Based on normal distribution assumption
    
    :param returns: Array of historical log returns
    :param portfolio_value: Current portfolio value
    :param confidence_level: Confidence level (0.90-0.99)
    :param horizon: Time horizon in days
    :return: Parametric VaR value (always positive)
    """
    try:
        # Validate inputs
        if len(returns) < 10:
            raise ValueError("Insufficient data for calculation (min 10 data points)")
        if not 0.90 <= confidence_level <= 0.99:
            raise ValueError("Confidence level must be between 0.90 and 0.99")
        if portfolio_value <= 0:
            raise ValueError("Portfolio value must be positive")
        if horizon <= 0:
            raise ValueError("Time horizon must be positive")

        # Calculate mean and standard deviation of returns
        mean = np.mean(returns)
        std = np.std(returns)
        
        # Calculate z-score based on confidence level
        z_score = norm.ppf(1 - confidence_level)
        
        # Calculate VaR using industry-standard formula
        # Formula: VaR = Portfolio Value × |Z × σ × √T - μ × T|
        var = portfolio_value * abs(z_score * std * np.sqrt(horizon) - mean * horizon)
        
        # Ensure non-negative VaR
        var = max(0, var)
        
        logger.info(
            f"Parametric VaR calculated: ₹{var:,.2f} at {confidence_level*100:.1f}% confidence "
            f"over {horizon} days (μ={mean:.6f}, σ={std:.6f})"
        )
        return var
        
    except Exception as e:
        logger.error(f"Parametric VaR calculation failed: {str(e)}")
        raise RuntimeError(f"Parametric VaR calculation error: {str(e)}")
