"""
Kata10: TDD practice - adding get_temperature_stats() feature to WeatherFilter.

Three red-green-refactor cycles:
  Cycle 1: average temperature
  Cycle 2: min/max temperature
  Cycle 3: empty records edge case
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "Kata1"))

from weather_filter import WeatherFilter


SAMPLE_RECORDS = [
    {"station": "A", "temperature": "10.0"},
    {"station": "B", "temperature": "20.0"},
    {"station": "C", "temperature": "30.0"},
]


def make_filter():
    """Return a WeatherFilter with a no-op log path."""
    log_path = Path(__file__).parent / "test_weather.log"
    return WeatherFilter(log_path)


# ---------------------------------------------------------------------------
# Cycle 1 — average temperature
# ---------------------------------------------------------------------------

def test_stats_returns_correct_average():
    wf = make_filter()
    stats = wf.get_temperature_stats(SAMPLE_RECORDS)
    assert stats["average"] == 20.0


# ---------------------------------------------------------------------------
# Cycle 2 — filter by station name
# ---------------------------------------------------------------------------

def test_filter_by_station_returns_matching_records():
    wf = make_filter()
    result = wf.filter_by_station(SAMPLE_RECORDS, "B")
    assert len(result) == 1
    assert result[0]["station"] == "B"
