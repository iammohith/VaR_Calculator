import numpy as np
import logging

logger = logging.getLogger(__name__)

def calculate_monte_carlo_var(returns, portfolio_value, confidence_level=0.95, horizon=1, simulations=10000):
    """
    Calculate Value at Risk using Monte Carlo simulation.
    
    Industry Standards:
    - Assumes lognormal distribution of stock prices
    - Uses geometric Brownian motion model
    - Properly scales volatility with time
    - Represents loss as positive value
    - Based on Black-Scholes model assumptions
    
    :param returns: Array of historical log returns
    :param portfolio_value: Current portfolio value
    :param confidence_level: Confidence level (0.90-0.99)
    :param horizon: Time horizon in days
    :param simulations: Number of simulations
    :return: Monte Carlo VaR value (always positive)
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
        if simulations <= 1000:
            raise ValueError("Minimum 1000 simulations required")
        
        # Convert daily returns to annual basis (252 trading days)
        daily_mean = np.mean(returns)
        daily_std = np.std(returns)
        annual_mean = daily_mean * 252
        annual_std = daily_std * np.sqrt(252)
        
        # Convert horizon to years
        horizon_years = horizon / 252.0
        
        # Simulate future returns using geometric Brownian motion
        # S_t = S_0 * exp((μ - 0.5σ²)t + σW_t)
        drift = (annual_mean - 0.5 * annual_std**2) * horizon_years
        volatility = annual_std * np.sqrt(horizon_years)
        
        # Generate random shocks
        random_shocks = np.random.normal(0, 1, simulations)
        
        # Calculate future prices
        future_prices = portfolio_value * np.exp(drift + volatility * random_shocks)
        
        # Calculate losses (positive values represent losses)
        losses = portfolio_value - future_prices
        
        # Calculate VaR as the loss at the confidence level
        var = np.percentile(losses, 100 * confidence_level)
        
        # Ensure non-negative VaR
        var = max(0, var)
        
        logger.info(
            f"Monte Carlo VaR calculated: ₹{var:,.2f} at {confidence_level*100:.1f}% confidence "
            f"over {horizon} days (μ={annual_mean:.6f}, σ={annual_std:.6f}, sims={simulations})"
        )
        return var
        
    except Exception as e:
        logger.error(f"Monte Carlo VaR calculation failed: {str(e)}")
        raise RuntimeError(f"Monte Carlo VaR calculation error: {str(e)}")
