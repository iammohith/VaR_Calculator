class DataFetchError(Exception):
    """Exception raised for errors in data fetching"""
    pass

class InvalidConfidenceLevel(Exception):
    """Exception raised for invalid confidence level"""
    pass

class CalculationError(Exception):
    """Exception raised for errors in VaR calculation"""
    pass
