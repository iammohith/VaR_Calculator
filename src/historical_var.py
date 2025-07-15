import numpy as np
import logging

logger = logging.getLogger(__name__)

def calculate_historical_var(returns, portfolio_value, confidence_level=0.95, horizon=1):
    """
    Calculate Value at Risk using historical simulation method.
    
    Industry Standards:
    - Uses actual historical returns without distribution assumptions
    - Properly handles multi-day horizons with block bootstrapping
    - Represents loss as positive value
    - Based on empirical distribution of returns
    
    :param returns: Array of historical log returns
    :param portfolio_value: Current portfolio value
    :param confidence_level: Confidence level (0.90-0.99)
    :param horizon: Time horizon in days
    :return: Historical VaR value (always positive)
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
        
        # For multi-day horizon, use block bootstrapping
        if horizon > 1:
            horizon_returns = []
            n = len(returns)
            # Ensure we have enough data for block sampling
            if n < horizon:
                raise ValueError("Insufficient data for horizon period")
                
            # Generate 10,000 samples of horizon-period returns
            for _ in range(10000):
                # Random start index for a block of 'horizon' days
                start_idx = np.random.randint(0, n - horizon)
                # Sum of log returns over the horizon period
                cumulative_return = np.sum(returns[start_idx:start_idx+horizon])
                horizon_returns.append(cumulative_return)
            returns_dist = np.array(horizon_returns)
        else:
            returns_dist = returns
        
        # Calculate portfolio values after horizon
        portfolio_values = portfolio_value * np.exp(returns_dist)
        
        # Calculate losses (positive values represent losses)
        losses = portfolio_value - portfolio_values
        
        # Calculate VaR as the loss at the confidence level
        # For 99% confidence, we take the 99th percentile of losses
        var = np.percentile(losses, 100 * confidence_level)
        
        # Ensure non-negative VaR
        var = max(0, var)
        
        logger.info(
            f"Historical VaR calculated: ₹{var:,.2f} at {confidence_level*100:.1f}% confidence "
            f"over {horizon} days"
        )
        return var
        
    except Exception as e:
        logger.error(f"Historical VaR calculation failed: {str(e)}")
        raise RuntimeError(f"Historical VaR calculation error: {str(e)}")
