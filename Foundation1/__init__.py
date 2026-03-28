"""Foundation1 package marker.

Contains FRED helper utilities.
"""

from .FRED_helper import get_fred_series, get_api_key

__all__ = ["get_fred_series", "get_api_key"]
