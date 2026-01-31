"""
FRED Data Retrieval Script

Federal Reserve Economic Data (FRED) API Integration
API Documentation: https://fred.stlouisfed.org/docs/api/fred/

This script demonstrates accessing economic time series data from FRED,
showcasing architectural patterns for time series data retrieval and storage.

Setup:
1. Register for a free API key at: https://fred.stlouisfed.org/docs/api/api_key.html
2. Set environment variable: FRED_API_KEY=your_key_here
3. Run: python FRED_Data_Retrieval.py

Dependencies:
    pip install requests python-dotenv
"""

import os
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from typing import List, Optional
from urllib.parse import urlencode
from pathlib import Path

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: 'requests' not installed. Install with: pip install requests")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: 'python-dotenv' not installed. Install with: pip install python-dotenv")


# =============================================================================
# DOMAIN MODELS - Time Series Data
# =============================================================================


@dataclass
class Observation:
    """Single observation in a time series."""
    date: date
    value: float | None
    realtime_start: date | None = None
    realtime_end: date | None = None
    
    def __post_init__(self):
        """Convert string dates to date objects if needed."""
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, "%Y-%m-%d").date()
        if isinstance(self.realtime_start, str):
            self.realtime_start = datetime.strptime(self.realtime_start, "%Y-%m-%d").date()
        if isinstance(self.realtime_end, str):
            self.realtime_end = datetime.strptime(self.realtime_end, "%Y-%m-%d").date()
    
    def to_dict(self) -> dict:
        """Convert to dictionary with ISO format dates."""
        return {
            "date": self.date.isoformat(),
            "value": self.value,
            "realtime_start": self.realtime_start.isoformat() if self.realtime_start else None,
            "realtime_end": self.realtime_end.isoformat() if self.realtime_end else None,
        }


@dataclass
class Series:
    """Economic time series metadata."""
    id: str
    title: str
    units: str
    frequency: str
    seasonal_adjustment: str
    last_updated: datetime
    popularity: int = 0
    notes: str = ""
    observations: List[Observation] = field(default_factory=list)
    
    def __post_init__(self):
        """Convert string datetime to datetime object if needed."""
        if isinstance(self.last_updated, str):
            self.last_updated = datetime.fromisoformat(self.last_updated.replace('Z', '+00:00'))
    
    @property
    def observation_count(self) -> int:
        """Number of observations in the series."""
        return len(self.observations)
    
    @property
    def date_range(self) -> tuple[date, date] | None:
        """First and last observation dates."""
        if not self.observations:
            return None
        return (self.observations[0].date, self.observations[-1].date)
    
    def get_latest_value(self) -> float | None:
        """Get the most recent non-null observation value."""
        for obs in reversed(self.observations):
            if obs.value is not None:
                return obs.value
        return None


@dataclass
class Category:
    """FRED data category."""
    id: int
    name: str
    parent_id: int | None = None


# =============================================================================
# FRED API CLIENT
# =============================================================================


class FREDClient:
    """Client for accessing Federal Reserve Economic Data API."""
    
    BASE_URL = "https://api.stlouisfed.org/fred"
    
    def __init__(self, api_key: str | None = None):
        """Initialize FRED client with API key.
        
        Args:
            api_key: FRED API key. If None, reads from FRED_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        if not self.api_key:
            raise ValueError(
                "FRED API key required. Set FRED_API_KEY environment variable "
                "or pass api_key parameter. Get key at: "
                "https://fred.stlouisfed.org/docs/api/api_key.html"
            )
        
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library required. Install with: pip install requests")
    
    def _make_request(self, endpoint: str, params: dict) -> dict:
        """Make API request to FRED.
        
        Args:
            endpoint: API endpoint (e.g., 'series/observations')
            params: Query parameters
            
        Returns:
            JSON response as dictionary
        """
        params["api_key"] = self.api_key
        params["file_type"] = "json"
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
    
    def get_series_info(self, series_id: str) -> Series:
        """Get metadata for a specific series.
        
        Args:
            series_id: FRED series ID (e.g., 'GDP', 'UNRATE')
            
        Returns:
            Series object with metadata
        """
        data = self._make_request("series", {"series_id": series_id})
        series_data = data["seriess"][0]
        
        return Series(
            id=series_data["id"],
            title=series_data["title"],
            units=series_data["units"],
            frequency=series_data["frequency"],
            seasonal_adjustment=series_data["seasonal_adjustment"],
            last_updated=series_data["last_updated"],
            popularity=series_data.get("popularity", 0),
            notes=series_data.get("notes", ""),
        )
    
    def get_series_observations(
        self,
        series_id: str,
        observation_start: str | None = None,
        observation_end: str | None = None,
        limit: int | None = None,
    ) -> List[Observation]:
        """Get observations for a specific series.
        
        Args:
            series_id: FRED series ID
            observation_start: Start date (YYYY-MM-DD)
            observation_end: End date (YYYY-MM-DD)
            limit: Maximum number of observations to retrieve
            
        Returns:
            List of Observation objects
        """
        params = {"series_id": series_id}
        
        if observation_start:
            params["observation_start"] = observation_start
        if observation_end:
            params["observation_end"] = observation_end
        if limit:
            params["limit"] = limit
        
        data = self._make_request("series/observations", params)
        
        observations = []
        for obs in data["observations"]:
            value = None if obs["value"] == "." else float(obs["value"])
            observations.append(
                Observation(
                    date=obs["date"],
                    value=value,
                    realtime_start=obs.get("realtime_start"),
                    realtime_end=obs.get("realtime_end"),
                )
            )
        
        return observations
    
    def get_series(
        self,
        series_id: str,
        observation_start: str | None = None,
        observation_end: str | None = None,
        limit: int | None = None,
    ) -> Series:
        """Get complete series with metadata and observations.
        
        Args:
            series_id: FRED series ID
            observation_start: Start date (YYYY-MM-DD)
            observation_end: End date (YYYY-MM-DD)
            limit: Maximum number of observations
            
        Returns:
            Complete Series object
        """
        series = self.get_series_info(series_id)
        series.observations = self.get_series_observations(
            series_id, observation_start, observation_end, limit
        )
        return series
    
    def search_series(self, search_text: str, limit: int = 10) -> List[dict]:
        """Search for series by text.
        
        Args:
            search_text: Search query
            limit: Maximum number of results
            
        Returns:
            List of series metadata dictionaries
        """
        params = {
            "search_text": search_text,
            "limit": limit,
        }
        
        data = self._make_request("series/search", params)
        return data.get("seriess", [])
    
    def get_categories(self, category_id: int = 0) -> List[Category]:
        """Get child categories for a given category.
        
        Args:
            category_id: Parent category ID (0 for root)
            
        Returns:
            List of Category objects
        """
        params = {"category_id": category_id}
        data = self._make_request("category/children", params)
        
        return [
            Category(
                id=cat["id"],
                name=cat["name"],
                parent_id=cat.get("parent_id"),
            )
            for cat in data.get("categories", [])
        ]


# =============================================================================
# DATA PERSISTENCE
# =============================================================================


class SeriesRepository:
    """Repository for saving and loading Series data."""
    
    def __init__(self, data_dir: Path = Path("./fred_data")):
        """Initialize repository with data directory."""
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
    
    def save_series(self, series: Series) -> Path:
        """Save series to JSON file.
        
        Args:
            series: Series to save
            
        Returns:
            Path to saved file
        """
        filepath = self.data_dir / f"{series.id}.json"
        
        data = {
            "id": series.id,
            "title": series.title,
            "units": series.units,
            "frequency": series.frequency,
            "seasonal_adjustment": series.seasonal_adjustment,
            "last_updated": series.last_updated.isoformat(),
            "popularity": series.popularity,
            "notes": series.notes,
            "observations": [obs.to_dict() for obs in series.observations],
        }
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        
        return filepath
    
    def load_series(self, series_id: str) -> Series | None:
        """Load series from JSON file.
        
        Args:
            series_id: ID of series to load
            
        Returns:
            Series object or None if not found
        """
        filepath = self.data_dir / f"{series_id}.json"
        
        if not filepath.exists():
            return None
        
        with open(filepath, "r") as f:
            data = json.load(f)
        
        observations = [
            Observation(
                date=obs["date"],
                value=obs["value"],
                realtime_start=obs.get("realtime_start"),
                realtime_end=obs.get("realtime_end"),
            )
            for obs in data["observations"]
        ]
        
        return Series(
            id=data["id"],
            title=data["title"],
            units=data["units"],
            frequency=data["frequency"],
            seasonal_adjustment=data["seasonal_adjustment"],
            last_updated=data["last_updated"],
            popularity=data.get("popularity", 0),
            notes=data.get("notes", ""),
            observations=observations,
        )


# =============================================================================
# EXAMPLE USAGE
# =============================================================================


def demonstrate_basic_retrieval():
    """Demonstrate basic data retrieval from FRED."""
    print("\n" + "=" * 70)
    print("FRED API - Basic Data Retrieval Demo")
    print("=" * 70)
    
    try:
        client = FREDClient()
        
        # Example 1: GDP
        print("\n1. Gross Domestic Product (GDP)")
        print("-" * 70)
        gdp = client.get_series("GDP", limit=5)
        print(f"Series: {gdp.title}")
        print(f"Units: {gdp.units}")
        print(f"Frequency: {gdp.frequency}")
        print(f"Last Updated: {gdp.last_updated}")
        print(f"Latest Value: {gdp.get_latest_value()}")
        print(f"\nRecent observations:")
        for obs in gdp.observations[-5:]:
            print(f"  {obs.date}: ${obs.value:,.0f} {gdp.units}" if obs.value else f"  {obs.date}: N/A")
        
        # Example 2: Unemployment Rate
        print("\n2. Unemployment Rate (UNRATE)")
        print("-" * 70)
        unrate = client.get_series("UNRATE", observation_start="2020-01-01", limit=10)
        print(f"Series: {unrate.title}")
        print(f"Units: {unrate.units}")
        print(f"Latest Value: {unrate.get_latest_value()}%")
        print(f"\nRecent observations:")
        for obs in unrate.observations[-10:]:
            print(f"  {obs.date}: {obs.value}%" if obs.value else f"  {obs.date}: N/A")
        
        # Example 3: Federal Funds Rate
        print("\n3. Federal Funds Effective Rate (FEDFUNDS)")
        print("-" * 70)
        fedfunds = client.get_series("FEDFUNDS", limit=12)
        print(f"Series: {fedfunds.title}")
        print(f"Units: {fedfunds.units}")
        print(f"Latest Value: {fedfunds.get_latest_value()}%")
        print(f"\nLast 12 months:")
        for obs in fedfunds.observations[-12:]:
            print(f"  {obs.date}: {obs.value}%" if obs.value else f"  {obs.date}: N/A")
        
        # Save data to files
        print("\n4. Saving Data to Files")
        print("-" * 70)
        repo = SeriesRepository()
        for series in [gdp, unrate, fedfunds]:
            filepath = repo.save_series(series)
            print(f"Saved {series.id} to {filepath}")
        
        # Search for series
        print("\n5. Searching for Series")
        print("-" * 70)
        results = client.search_series("inflation", limit=5)
        print(f"Found {len(results)} results for 'inflation':")
        for result in results:
            print(f"  {result['id']}: {result['title']}")
        
        # Browse categories
        print("\n6. Browse Categories")
        print("-" * 70)
        categories = client.get_categories(0)
        print("Top-level FRED categories:")
        for cat in categories[:10]:
            print(f"  {cat.id}: {cat.name}")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nTo use this script:")
        print("1. Get a free API key: https://fred.stlouisfed.org/docs/api/api_key.html")
        print("2. Set environment variable: FRED_API_KEY=your_key_here")
        print("   Or create a .env file with: FRED_API_KEY=your_key_here")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        raise


def demonstrate_time_series_analysis():
    """Demonstrate basic time series analysis on FRED data."""
    print("\n" + "=" * 70)
    print("FRED API - Time Series Analysis Demo")
    print("=" * 70)
    
    try:
        client = FREDClient()
        
        # Get inflation data (CPI)
        print("\n1. Consumer Price Index (CPIAUCSL)")
        print("-" * 70)
        cpi = client.get_series("CPIAUCSL", observation_start="2020-01-01")
        print(f"Series: {cpi.title}")
        print(f"Observations: {cpi.observation_count}")
        print(f"Date Range: {cpi.date_range}")
        
        # Calculate year-over-year change
        print(f"\nYear-over-year percentage change:")
        observations = [obs for obs in cpi.observations if obs.value is not None]
        for i in range(len(observations) - 12, len(observations)):
            if i >= 12:
                current = observations[i]
                previous = observations[i - 12]
                if current.value and previous.value:
                    yoy_change = ((current.value - previous.value) / previous.value) * 100
                    print(f"  {current.date}: {yoy_change:.2f}%")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_basic_retrieval()
    
    # Uncomment to run time series analysis
    # demonstrate_time_series_analysis()
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\nNext Steps:")
    print("- Explore more series: https://fred.stlouisfed.org/")
    print("- Check saved data in ./fred_data/ directory")
    print("- Modify script to analyze different economic indicators")
    print("- Implement revision tracking with ALFRED API")
