"""
Testing and Mocking with unittest Example

This module demonstrates unittest fundamentals using the airport domain model.
It includes tests for the domain classes, mocking external dependencies,
and various testing patterns.

Run with: python -m unittest example.py -v
Or:       python example.py
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, create_autospec, call
from dataclasses import dataclass, field
from typing import Protocol
from abc import ABC, abstractmethod
import asyncio


# =============================================================================
# DOMAIN MODEL (Code Under Test)
# =============================================================================


@dataclass
class Runway:
    """Airport runway."""
    identifier: str
    length_ft: int
    surface: str = "concrete"


@dataclass
class WeatherReport:
    """Weather data for an airport."""
    stationid: str
    temperature: float
    conditions: str
    wind_speed: int = 0


@dataclass
class Airport:
    """Airport with runways and validation."""
    stationid: str
    name: str
    city: str = ""
    state: str = ""
    _runways: list[Runway] = field(default_factory=list, repr=False)
    
    def __post_init__(self):
        if not self.stationid:
            raise ValueError("stationid cannot be empty")
        if len(self.stationid) != 4:
            raise ValueError("stationid must be exactly 4 characters")
        if not self.stationid.isupper():
            raise ValueError("stationid must be uppercase")
    
    @property
    def runways(self) -> list[Runway]:
        return self._runways.copy()
    
    @property
    def longest_runway(self) -> int:
        if not self._runways:
            return 0
        return max(r.length_ft for r in self._runways)
    
    def add_runway(self, identifier: str, length_ft: int, surface: str = "concrete") -> None:
        self._runways.append(Runway(identifier, length_ft, surface))
    
    def can_land(self, required_runway_length: int) -> bool:
        return self.longest_runway >= required_runway_length


class WeatherService(Protocol):
    """Protocol for weather service."""
    def fetch_weather(self, stationid: str) -> WeatherReport: ...


class AirportRepository(Protocol):
    """Protocol for airport data access."""
    def get_by_stationid(self, stationid: str) -> Airport | None: ...
    def save(self, airport: Airport) -> Airport: ...


class AirportManager:
    """Manages airport operations with injected dependencies."""
    
    def __init__(self, repository: AirportRepository, weather_service: WeatherService):
        self._repo = repository
        self._weather = weather_service
    
    def get_airport_with_weather(self, stationid: str) -> dict:
        airport = self._repo.get_by_stationid(stationid)
        if not airport:
            raise ValueError(f"Airport {stationid} not found")
        
        weather = self._weather.fetch_weather(stationid)
        
        return {
            "airport": airport,
            "weather": weather,
            "can_land_737": airport.can_land(6000),
        }
    
    def create_airport(self, stationid: str, name: str) -> Airport:
        airport = Airport(stationid, name)
        return self._repo.save(airport)


# =============================================================================
# BASIC TESTS
# =============================================================================


class TestAirportCreation(unittest.TestCase):
    """Tests for Airport creation and validation."""
    
    def test_creation_with_valid_data(self):
        """Airport can be created with valid data."""
        airport = Airport("KAMA", "Amarillo International")
        
        self.assertEqual(airport.stationid, "KAMA")
        self.assertEqual(airport.name, "Amarillo International")
    
    def test_creation_with_all_fields(self):
        """Airport can be created with all optional fields."""
        airport = Airport("KAMA", "Amarillo International", "Amarillo", "TX")
        
        self.assertEqual(airport.city, "Amarillo")
        self.assertEqual(airport.state, "TX")
    
    def test_empty_stationid_raises_valueerror(self):
        """Empty stationid raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Airport("", "Test Airport")
        
        self.assertIn("empty", str(context.exception))
    
    def test_short_stationid_raises_valueerror(self):
        """Short stationid raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Airport("KAM", "Test Airport")
        
        self.assertIn("4 characters", str(context.exception))
    
    def test_lowercase_stationid_raises_valueerror(self):
        """Lowercase stationid raises ValueError."""
        with self.assertRaises(ValueError):
            Airport("kama", "Test Airport")


class TestAirportRunways(unittest.TestCase):
    """Tests for Airport runway operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.airport = Airport("KAMA", "Amarillo International")
    
    def test_new_airport_has_no_runways(self):
        """New airport starts with no runways."""
        self.assertEqual(len(self.airport.runways), 0)
    
    def test_add_runway_increases_count(self):
        """Adding a runway increases the count."""
        self.airport.add_runway("04/22", 13502)
        
        self.assertEqual(len(self.airport.runways), 1)
    
    def test_add_multiple_runways(self):
        """Multiple runways can be added."""
        self.airport.add_runway("04/22", 13502)
        self.airport.add_runway("13/31", 7898)
        
        self.assertEqual(len(self.airport.runways), 2)
    
    def test_runway_has_correct_data(self):
        """Added runway has correct data."""
        self.airport.add_runway("04/22", 13502, "asphalt")
        
        runway = self.airport.runways[0]
        self.assertEqual(runway.identifier, "04/22")
        self.assertEqual(runway.length_ft, 13502)
        self.assertEqual(runway.surface, "asphalt")
    
    def test_runways_returns_copy(self):
        """Runways property returns a copy, not the internal list."""
        self.airport.add_runway("04/22", 13502)
        
        runways = self.airport.runways
        runways.clear()  # Modify the copy
        
        self.assertEqual(len(self.airport.runways), 1)  # Original unchanged


class TestLongestRunway(unittest.TestCase):
    """Tests for longest_runway property."""
    
    def setUp(self):
        self.airport = Airport("KAMA", "Test")
    
    def test_no_runways_returns_zero(self):
        """No runways returns 0."""
        self.assertEqual(self.airport.longest_runway, 0)
    
    def test_one_runway_returns_its_length(self):
        """Single runway returns its length."""
        self.airport.add_runway("04/22", 13502)
        
        self.assertEqual(self.airport.longest_runway, 13502)
    
    def test_multiple_runways_returns_longest(self):
        """Multiple runways returns the longest."""
        self.airport.add_runway("04/22", 13502)
        self.airport.add_runway("13/31", 7898)
        
        self.assertEqual(self.airport.longest_runway, 13502)
    
    def test_longest_runway_not_first(self):
        """Returns longest even if not added first."""
        self.airport.add_runway("13/31", 7898)
        self.airport.add_runway("04/22", 13502)
        
        self.assertEqual(self.airport.longest_runway, 13502)


class TestCanLand(unittest.TestCase):
    """Tests for can_land method."""
    
    def setUp(self):
        self.airport = Airport("KAMA", "Test")
        self.airport.add_runway("04/22", 10000)
    
    def test_can_land_with_shorter_requirement(self):
        """Can land when required length is less than available."""
        self.assertTrue(self.airport.can_land(8000))
    
    def test_can_land_with_exact_requirement(self):
        """Can land when required length equals available."""
        self.assertTrue(self.airport.can_land(10000))
    
    def test_cannot_land_with_longer_requirement(self):
        """Cannot land when required length exceeds available."""
        self.assertFalse(self.airport.can_land(12000))
    
    def test_cannot_land_with_no_runways(self):
        """Cannot land when airport has no runways."""
        empty_airport = Airport("KLBB", "Test")
        
        self.assertFalse(empty_airport.can_land(1000))


# =============================================================================
# PARAMETERIZED TESTS
# =============================================================================


class TestStationIdValidation(unittest.TestCase):
    """Parameterized tests for stationid validation."""
    
    def test_valid_stationids(self):
        """Various valid stationids are accepted."""
        valid_ids = ["KAMA", "KLBB", "KMAF", "KDFW", "EGLL", "RJTT"]
        
        for stationid in valid_ids:
            with self.subTest(stationid=stationid):
                airport = Airport(stationid, "Test")
                self.assertEqual(airport.stationid, stationid)
    
    def test_invalid_stationids(self):
        """Various invalid stationids are rejected."""
        invalid_ids = [
            ("", "empty"),
            ("K", "too short"),
            ("KAM", "too short"),
            ("KAMAA", "too long"),
            ("kama", "lowercase"),
            ("Kama", "mixed case"),
            ("1234", "all digits"),  # This might actually be valid depending on rules
        ]
        
        for stationid, reason in invalid_ids:
            with self.subTest(stationid=stationid, reason=reason):
                with self.assertRaises(ValueError):
                    Airport(stationid, "Test")


# =============================================================================
# MOCKING EXAMPLES
# =============================================================================


class TestAirportManagerWithMocks(unittest.TestCase):
    """Tests using mocks for dependencies."""
    
    def setUp(self):
        """Set up mocks for each test."""
        self.mock_repo = Mock(spec=AirportRepository)
        self.mock_weather = Mock(spec=WeatherService)
        self.manager = AirportManager(self.mock_repo, self.mock_weather)
    
    def test_get_airport_with_weather_success(self):
        """Successfully retrieves airport with weather."""
        # Arrange
        test_airport = Airport("KAMA", "Amarillo International")
        test_airport.add_runway("04/22", 10000)
        test_weather = WeatherReport("KAMA", 72.0, "Clear", 10)
        
        self.mock_repo.get_by_stationid.return_value = test_airport
        self.mock_weather.fetch_weather.return_value = test_weather
        
        # Act
        result = self.manager.get_airport_with_weather("KAMA")
        
        # Assert
        self.assertEqual(result["airport"].stationid, "KAMA")
        self.assertEqual(result["weather"].temperature, 72.0)
        self.assertTrue(result["can_land_737"])
        
        # Verify mock calls
        self.mock_repo.get_by_stationid.assert_called_once_with("KAMA")
        self.mock_weather.fetch_weather.assert_called_once_with("KAMA")
    
    def test_get_airport_not_found_raises(self):
        """Raises ValueError when airport not found."""
        self.mock_repo.get_by_stationid.return_value = None
        
        with self.assertRaises(ValueError) as context:
            self.manager.get_airport_with_weather("KXYZ")
        
        self.assertIn("KXYZ", str(context.exception))
        self.assertIn("not found", str(context.exception))
    
    def test_create_airport_calls_save(self):
        """Create airport saves via repository."""
        expected_airport = Airport("KLBB", "Lubbock International")
        self.mock_repo.save.return_value = expected_airport
        
        result = self.manager.create_airport("KLBB", "Lubbock International")
        
        self.assertEqual(result.stationid, "KLBB")
        self.mock_repo.save.assert_called_once()
        
        # Verify the airport passed to save
        saved_airport = self.mock_repo.save.call_args[0][0]
        self.assertEqual(saved_airport.stationid, "KLBB")


class TestMockingPatterns(unittest.TestCase):
    """Demonstrates various mocking patterns."""
    
    def test_basic_mock(self):
        """Basic mock with return value."""
        mock = Mock()
        mock.get_data.return_value = {"key": "value"}
        
        result = mock.get_data()
        
        self.assertEqual(result["key"], "value")
        mock.get_data.assert_called_once()
    
    def test_mock_with_side_effect_exception(self):
        """Mock that raises an exception."""
        mock = Mock()
        mock.fetch.side_effect = ConnectionError("Network error")
        
        with self.assertRaises(ConnectionError):
            mock.fetch()
    
    def test_mock_with_side_effect_values(self):
        """Mock that returns different values on each call."""
        mock = Mock()
        mock.get_next.side_effect = [1, 2, 3]
        
        self.assertEqual(mock.get_next(), 1)
        self.assertEqual(mock.get_next(), 2)
        self.assertEqual(mock.get_next(), 3)
    
    def test_mock_with_side_effect_function(self):
        """Mock with custom side effect function."""
        mock = Mock()
        mock.transform.side_effect = lambda x: x.upper()
        
        self.assertEqual(mock.transform("kama"), "KAMA")
    
    def test_mock_call_args(self):
        """Inspecting mock call arguments."""
        mock = Mock()
        mock("KAMA", runway_length=10000)
        mock("KLBB", runway_length=8000)
        
        # Check all calls
        self.assertEqual(mock.call_count, 2)
        
        # Check specific calls
        mock.assert_any_call("KAMA", runway_length=10000)
        
        # Check call order
        mock.assert_has_calls([
            call("KAMA", runway_length=10000),
            call("KLBB", runway_length=8000),
        ])
    
    def test_magic_mock(self):
        """MagicMock supports magic methods."""
        mock = MagicMock()
        mock.__len__.return_value = 5
        mock.__getitem__.return_value = "item"
        
        self.assertEqual(len(mock), 5)
        self.assertEqual(mock[0], "item")
    
    def test_autospec(self):
        """Autospec validates method signatures."""
        mock = create_autospec(Airport)
        
        # This would raise TypeError if wrong signature
        mock.can_land(10000)
        mock.can_land.assert_called_with(10000)


class TestPatchDecorator(unittest.TestCase):
    """Tests using @patch decorator."""
    
    @patch.object(Airport, 'can_land')
    def test_patch_method(self, mock_can_land):
        """Patch a specific method."""
        mock_can_land.return_value = True
        
        airport = Airport("KAMA", "Test")
        result = airport.can_land(99999)  # Would normally be False
        
        self.assertTrue(result)
        mock_can_land.assert_called_once_with(99999)


# =============================================================================
# FIXTURES EXAMPLE
# =============================================================================


class TestWithFixtures(unittest.TestCase):
    """Demonstrates setUp/tearDown patterns."""
    
    @classmethod
    def setUpClass(cls):
        """Run once before all tests in this class."""
        cls.shared_data = {"initialized": True}
        print("\n  [setUpClass] Creating shared resources")
    
    @classmethod
    def tearDownClass(cls):
        """Run once after all tests in this class."""
        print("\n  [tearDownClass] Cleaning shared resources")
    
    def setUp(self):
        """Run before each test."""
        self.airport = Airport("KAMA", "Test Airport")
        self.airport.add_runway("04/22", 10000)
    
    def tearDown(self):
        """Run after each test."""
        # Clean up if needed
        pass
    
    def test_uses_fixture(self):
        """Test that uses setUp fixture."""
        self.assertEqual(self.airport.stationid, "KAMA")
        self.assertEqual(len(self.airport.runways), 1)
    
    def test_modifies_fixture(self):
        """Each test gets fresh fixture."""
        self.airport.add_runway("13/31", 8000)
        self.assertEqual(len(self.airport.runways), 2)
    
    def test_fixture_is_fresh(self):
        """Verify fixture wasn't affected by previous test."""
        # This should still be 1, not 2
        self.assertEqual(len(self.airport.runways), 1)


# =============================================================================
# ASYNC TESTS
# =============================================================================


class TestAsyncOperations(unittest.IsolatedAsyncioTestCase):
    """Tests for async code (Python 3.8+)."""
    
    async def test_async_operation(self):
        """Test async function."""
        async def async_fetch():
            await asyncio.sleep(0.01)
            return {"temp": 72}
        
        result = await async_fetch()
        self.assertEqual(result["temp"], 72)
    
    async def test_async_with_mock(self):
        """Test async function with mock."""
        mock = Mock()
        mock.fetch = Mock(return_value=asyncio.coroutine(lambda: {"temp": 72})())
        
        # For simpler async mocking, use AsyncMock (Python 3.8+)
        from unittest.mock import AsyncMock
        mock.fetch = AsyncMock(return_value={"temp": 72})
        
        result = await mock.fetch()
        self.assertEqual(result["temp"], 72)


# =============================================================================
# MAIN
# =============================================================================


def run_demo():
    """Run a demonstration of the tests."""
    print("=" * 70)
    print("TESTING AND MOCKING DEMONSTRATION")
    print("=" * 70)
    
    # Create a test suite with selected tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAirportCreation))
    suite.addTests(loader.loadTestsFromTestCase(TestAirportRunways))
    suite.addTests(loader.loadTestsFromTestCase(TestLongestRunway))
    suite.addTests(loader.loadTestsFromTestCase(TestCanLand))
    suite.addTests(loader.loadTestsFromTestCase(TestStationIdValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestAirportManagerWithMocks))
    suite.addTests(loader.loadTestsFromTestCase(TestMockingPatterns))
    suite.addTests(loader.loadTestsFromTestCase(TestWithFixtures))
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n  ✓ All tests passed!")
    else:
        print("\n  ✗ Some tests failed")
        for test, traceback in result.failures:
            print(f"\n  FAILED: {test}")
            print(traceback)
    
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
