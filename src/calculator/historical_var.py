import numpy as np
import pandas as pd

def calculate_historical_var(returns: pd.Series, portfolio_value: float, confidence: float) -> float:
    """
    Calculate VaR using historical simulation method
    """
    returns_sorted = returns.sort_values()
    var_index = int((1 - confidence) * len(returns_sorted))
    var = -returns_sorted.iloc[var_index] * portfolio_value
    return var
