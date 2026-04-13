# Testing and Mocking with unittest

Testing is essential for building reliable software. Python's `unittest` module provides a robust framework for writing and organizing tests. This guide covers unittest fundamentals, assertions, fixtures, mocking, and best practices.

## Table of Contents

1. [Why Test?](#why-test)
2. [unittest Basics](#unittest-basics)
3. [Test Discovery and Organization](#test-discovery-and-organization)
4. [Assertions](#assertions)
5. [Fixtures: setUp and tearDown](#fixtures-setup-and-teardown)
6. [Mocking with unittest.mock](#mocking-with-unittestmock)
7. [Testing Patterns](#testing-patterns)
8. [Best Practices](#best-practices)

---

## Why Test?

**Benefits of testing:**
- Catch bugs early before production
- Enable confident refactoring
- Serve as documentation
- Improve design (testable code is often better code)
- Reduce debugging time

**Types of tests:**

| Type | Scope | Speed | Purpose |
|------|-------|-------|---------|
| Unit | Single function/class | Fast | Test isolated logic |
| Integration | Multiple components | Medium | Test interactions |
| End-to-end | Entire system | Slow | Test user workflows |

This guide focuses on **unit tests** with unittest.

---

## unittest Basics

### Minimal Test

```python
import unittest

class TestExample(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)

if __name__ == "__main__":
    unittest.main()
```

### Running Tests

```bash
# Run all tests in a file
python -m unittest test_example.py

# Run all tests in a directory
python -m unittest discover

# Run specific test class
python -m unittest test_example.TestExample

# Run specific test method
python -m unittest test_example.TestExample.test_addition

# Verbose output
python -m unittest -v test_example.py
```

### Test Structure (AAA Pattern)

```python
def test_airport_creation(self):
    # Arrange - set up test data
    stationid = "KAMA"
    name = "Amarillo International"

    # Act - perform the action
    airport = Airport(stationid, name)

    # Assert - verify the result
    self.assertEqual(airport.stationid, "KAMA")
    self.assertEqual(airport.name, "Amarillo International")
```

---

## Test Discovery and Organization

### Project Structure

```
project/
├── src/
│   ├── __init__.py
│   ├── airport.py
│   └── weather.py
├── tests/
│   ├── __init__.py
│   ├── test_airport.py
│   └── test_weather.py
└── pyproject.toml
```

### Naming Conventions

- Test files: `test_*.py` or `*_test.py`
- Test classes: `Test*` (inherit from `unittest.TestCase`)
- Test methods: `test_*`

```python
# test_airport.py
import unittest
from src.airport import Airport

class TestAirport(unittest.TestCase):
    def test_creation_with_valid_data(self):
        ...

    def test_creation_with_invalid_stationid_raises(self):
        ...

    def test_longest_runway_with_no_runways(self):
        ...
```

### Test Discovery

```bash
# Discover and run all tests
python -m unittest discover

# Specify test directory
python -m unittest discover -s tests

# Specify pattern
python -m unittest discover -p "test_*.py"
```

---

## Assertions

### Basic Assertions

```python
import unittest

class TestAssertions(unittest.TestCase):

    def test_equality(self):
        self.assertEqual(1 + 1, 2)
        self.assertNotEqual(1 + 1, 3)

    def test_truthiness(self):
        self.assertTrue(1 < 2)
        self.assertFalse(1 > 2)

    def test_none(self):
        self.assertIsNone(None)
        self.assertIsNotNone("something")

    def test_identity(self):
        a = [1, 2, 3]
        b = a
        c = [1, 2, 3]
        self.assertIs(a, b)       # Same object
        self.assertIsNot(a, c)    # Different objects
        self.assertEqual(a, c)    # But equal values

    def test_membership(self):
        self.assertIn("KAMA", ["KAMA", "KLBB", "KMAF"])
        self.assertNotIn("KXYZ", ["KAMA", "KLBB", "KMAF"])

    def test_types(self):
        self.assertIsInstance(Airport("KAMA", "Test"), Airport)
        self.assertNotIsInstance("string", Airport)
```

### Numeric Assertions

```python
def test_numeric(self):
    # Approximate equality (for floats)
    self.assertAlmostEqual(0.1 + 0.2, 0.3, places=7)
    self.assertNotAlmostEqual(0.1, 0.2, places=1)

    # Comparison
    self.assertGreater(5, 3)
    self.assertGreaterEqual(5, 5)
    self.assertLess(3, 5)
    self.assertLessEqual(5, 5)
```

### Collection Assertions

```python
def test_collections(self):
    # Lists/sequences
    self.assertListEqual([1, 2, 3], [1, 2, 3])

    # Tuples
    self.assertTupleEqual((1, 2), (1, 2))

    # Sets
    self.assertSetEqual({1, 2, 3}, {3, 2, 1})

    # Dicts
    self.assertDictEqual({"a": 1}, {"a": 1})

    # Count comparison
    self.assertCountEqual([1, 2, 2, 3], [3, 2, 1, 2])  # Same elements, any order
```

### Exception Assertions

```python
def test_exceptions(self):
    # Check that exception is raised
    with self.assertRaises(ValueError):
        int("not a number")

    # Check exception message
    with self.assertRaises(ValueError) as context:
        raise ValueError("Invalid station ID")
    self.assertIn("Invalid", str(context.exception))

    # Using assertRaisesRegex
    with self.assertRaisesRegex(ValueError, r"Invalid.*ID"):
        raise ValueError("Invalid station ID")
```

### Custom Assertion Messages

```python
def test_with_message(self):
    airport = Airport("KAMA", "Test")
    self.assertEqual(
        airport.stationid,
        "KAMA",
        f"Expected KAMA but got {airport.stationid}"
    )
```

---

## Fixtures: setUp and tearDown

Fixtures prepare the test environment and clean up afterward.

### Method-Level Fixtures

```python
import unittest

class TestAirport(unittest.TestCase):

    def setUp(self):
        """Runs before EACH test method."""
        self.airport = Airport("KAMA", "Amarillo International")
        self.airport.add_runway("04/22", 13502)

    def tearDown(self):
        """Runs after EACH test method."""
        # Clean up resources if needed
        pass

    def test_stationid(self):
        self.assertEqual(self.airport.stationid, "KAMA")

    def test_has_runway(self):
        self.assertEqual(len(self.airport.runways), 1)
```

### Class-Level Fixtures

```python
import unittest

class TestAirportDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before any tests in this class."""
        cls.db_connection = create_test_database()

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests in this class."""
        cls.db_connection.close()

    def setUp(self):
        """Runs before each test."""
        self.db_connection.begin_transaction()

    def tearDown(self):
        """Runs after each test."""
        self.db_connection.rollback()
```

### Module-Level Fixtures

```python
def setUpModule():
    """Runs once before any tests in this module."""
    print("Setting up module...")

def tearDownModule():
    """Runs once after all tests in this module."""
    print("Tearing down module...")
```

---

## Mocking with unittest.mock

Mocking replaces real objects with controlled substitutes, enabling isolated unit testing.

### Basic Mock

```python
from unittest.mock import Mock

def test_basic_mock():
    # Create a mock object
    mock = Mock()

    # Configure return value
    mock.return_value = 42
    assert mock() == 42

    # Configure method return value
    mock.get_weather.return_value = {"temp": 72}
    assert mock.get_weather("KAMA") == {"temp": 72}

    # Verify calls
    mock.get_weather.assert_called_once_with("KAMA")
```

### Patching with @patch

```python
from unittest import TestCase
from unittest.mock import patch, Mock

class WeatherService:
    def fetch_weather(self, stationid: str) -> dict:
        # Makes real HTTP request
        pass

class AirportManager:
    def __init__(self, weather_service: WeatherService):
        self._weather = weather_service

    def get_conditions(self, stationid: str) -> str:
        data = self._weather.fetch_weather(stationid)
        return data.get("conditions", "Unknown")

class TestAirportManager(TestCase):

    @patch.object(WeatherService, 'fetch_weather')
    def test_get_conditions(self, mock_fetch):
        # Configure mock
        mock_fetch.return_value = {"conditions": "Clear", "temp": 72}

        # Test
        service = WeatherService()
        manager = AirportManager(service)
        result = manager.get_conditions("KAMA")

        # Verify
        self.assertEqual(result, "Clear")
        mock_fetch.assert_called_once_with("KAMA")
```

### Patching Imports

```python
# weather_client.py
import requests

def fetch_weather(stationid: str) -> dict:
    response = requests.get(f"https://api.weather.gov/stations/{stationid}")
    return response.json()

# test_weather_client.py
from unittest import TestCase
from unittest.mock import patch, Mock

class TestFetchWeather(TestCase):

    @patch('weather_client.requests.get')
    def test_fetch_weather(self, mock_get):
        # Configure mock response
        mock_response = Mock()
        mock_response.json.return_value = {"temp": 72}
        mock_get.return_value = mock_response

        # Test
        from weather_client import fetch_weather
        result = fetch_weather("KAMA")

        # Verify
        self.assertEqual(result["temp"], 72)
        mock_get.assert_called_once()
```

### Context Manager Patching

```python
def test_with_context_manager(self):
    with patch('weather_client.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"temp": 72}

        result = fetch_weather("KAMA")

        self.assertEqual(result["temp"], 72)
```

### MagicMock

`MagicMock` includes magic method defaults.

```python
from unittest.mock import MagicMock

def test_magic_mock():
    mock = MagicMock()

    # Magic methods work automatically
    len(mock)  # Returns 0
    mock[0]    # Returns another MagicMock

    # Configure magic method
    mock.__len__.return_value = 5
    assert len(mock) == 5
```

### Mock Call Assertions

```python
from unittest.mock import Mock, call

def test_call_assertions():
    mock = Mock()

    # Make calls
    mock("KAMA")
    mock("KLBB")
    mock("KMAF")

    # Assert called
    mock.assert_called()
    mock.assert_called_with("KMAF")  # Last call

    # Assert call count
    assert mock.call_count == 3

    # Assert call sequence
    mock.assert_has_calls([
        call("KAMA"),
        call("KLBB"),
        call("KMAF"),
    ])

    # Any order
    mock.assert_has_calls([
        call("KMAF"),
        call("KAMA"),
    ], any_order=True)
```

### Side Effects

```python
from unittest.mock import Mock

def test_side_effects():
    mock = Mock()

    # Raise exception
    mock.side_effect = ValueError("Invalid ID")
    with self.assertRaises(ValueError):
        mock()

    # Return different values on each call
    mock.side_effect = [1, 2, 3]
    assert mock() == 1
    assert mock() == 2
    assert mock() == 3

    # Custom function
    mock.side_effect = lambda x: x.upper()
    assert mock("kama") == "KAMA"
```

### Spec and Autospec

```python
from unittest.mock import Mock, create_autospec

class WeatherService:
    def fetch_weather(self, stationid: str) -> dict:
        pass

def test_with_spec():
    # Mock with spec - only allows real attributes
    mock = Mock(spec=WeatherService)
    mock.fetch_weather.return_value = {"temp": 72}

    # This works
    mock.fetch_weather("KAMA")

    # This raises AttributeError
    # mock.invalid_method()  # AttributeError!

def test_with_autospec():
    # Autospec validates argument signatures too
    mock = create_autospec(WeatherService)
    mock.fetch_weather.return_value = {"temp": 72}

    # This works
    mock.fetch_weather("KAMA")

    # This raises TypeError (wrong args)
    # mock.fetch_weather("KAMA", "extra")  # TypeError!
```

---

## Testing Patterns

### Testing Exceptions

```python
class TestAirportValidation(unittest.TestCase):

    def test_invalid_stationid_raises_valueerror(self):
        with self.assertRaises(ValueError) as context:
            Airport("", "Test Airport")

        self.assertIn("stationid", str(context.exception).lower())

    def test_none_stationid_raises_typeerror(self):
        with self.assertRaises(TypeError):
            Airport(None, "Test Airport")
```

### Testing with Dependency Injection

```python
# Production code designed for testability
class AirportManager:
    def __init__(self, weather_service, repository):
        self._weather = weather_service
        self._repo = repository

    def get_airport_with_weather(self, stationid: str) -> dict:
        airport = self._repo.get_by_stationid(stationid)
        weather = self._weather.fetch_weather(stationid)
        return {"airport": airport, "weather": weather}

# Test with mocks injected
class TestAirportManager(unittest.TestCase):

    def setUp(self):
        self.mock_weather = Mock()
        self.mock_repo = Mock()
        self.manager = AirportManager(self.mock_weather, self.mock_repo)

    def test_get_airport_with_weather(self):
        # Configure mocks
        self.mock_repo.get_by_stationid.return_value = Airport("KAMA", "Test")
        self.mock_weather.fetch_weather.return_value = {"temp": 72}

        # Test
        result = self.manager.get_airport_with_weather("KAMA")

        # Verify
        self.assertEqual(result["airport"].stationid, "KAMA")
        self.assertEqual(result["weather"]["temp"], 72)
```

### Parameterized Tests

```python
class TestAirportValidation(unittest.TestCase):

    def test_valid_stationids(self):
        valid_ids = ["KAMA", "KLBB", "KMAF", "KDFW"]

        for stationid in valid_ids:
            with self.subTest(stationid=stationid):
                airport = Airport(stationid, "Test")
                self.assertEqual(airport.stationid, stationid)

    def test_invalid_stationids(self):
        invalid_ids = ["", "K", "KAMA1", "kama", "12345"]

        for stationid in invalid_ids:
            with self.subTest(stationid=stationid):
                with self.assertRaises(ValueError):
                    Airport(stationid, "Test")
```

### Testing Async Code

```python
import unittest
import asyncio

class TestAsyncWeather(unittest.TestCase):

    def test_async_fetch(self):
        async def async_fetch():
            await asyncio.sleep(0.1)
            return {"temp": 72}

        result = asyncio.run(async_fetch())
        self.assertEqual(result["temp"], 72)

    # Or use IsolatedAsyncioTestCase (Python 3.8+)

class TestAsyncWeatherAsync(unittest.IsolatedAsyncioTestCase):

    async def test_async_fetch(self):
        await asyncio.sleep(0.1)
        self.assertTrue(True)
```

---

## Best Practices

### 1. Test One Thing Per Test

```python
# Bad - testing multiple things
def test_airport(self):
    airport = Airport("KAMA", "Test")
    self.assertEqual(airport.stationid, "KAMA")
    self.assertEqual(airport.name, "Test")
    airport.add_runway("04/22", 13502)
    self.assertEqual(len(airport.runways), 1)

# Good - focused tests
def test_airport_has_correct_stationid(self):
    airport = Airport("KAMA", "Test")
    self.assertEqual(airport.stationid, "KAMA")

def test_airport_has_correct_name(self):
    airport = Airport("KAMA", "Test")
    self.assertEqual(airport.name, "Test")

def test_add_runway_increases_count(self):
    airport = Airport("KAMA", "Test")
    airport.add_runway("04/22", 13502)
    self.assertEqual(len(airport.runways), 1)
```

### 2. Use Descriptive Test Names

```python
# Bad
def test1(self): ...
def test_airport(self): ...

# Good
def test_airport_creation_with_valid_data_succeeds(self): ...
def test_airport_creation_with_empty_stationid_raises_valueerror(self): ...
def test_longest_runway_returns_zero_when_no_runways(self): ...
```

### 3. Arrange-Act-Assert Pattern

```python
def test_can_land_with_sufficient_runway(self):
    # Arrange
    airport = Airport("KAMA", "Test")
    airport.add_runway("04/22", 13502)
    required_length = 10000

    # Act
    result = airport.can_land(required_length)

    # Assert
    self.assertTrue(result)
```

### 4. Don't Test Implementation Details

```python
# Bad - tests internal state
def test_runway_stored_in_list(self):
    airport = Airport("KAMA", "Test")
    airport.add_runway("04/22", 13502)
    self.assertIsInstance(airport._runways, list)  # Implementation detail!

# Good - tests behavior
def test_runway_is_retrievable_after_adding(self):
    airport = Airport("KAMA", "Test")
    airport.add_runway("04/22", 13502)
    runways = airport.runways
    self.assertEqual(len(runways), 1)
    self.assertEqual(runways[0].identifier, "04/22")
```

### 5. Keep Tests Fast

```python
# Bad - slow tests
def test_weather_fetch(self):
    # Actually hits network
    weather = WeatherService().fetch("KAMA")
    self.assertIsNotNone(weather)

# Good - mock external dependencies
@patch('weather_service.requests.get')
def test_weather_fetch(self, mock_get):
    mock_get.return_value.json.return_value = {"temp": 72}
    weather = WeatherService().fetch("KAMA")
    self.assertEqual(weather["temp"], 72)
```

### 6. Use Fixtures Appropriately

```python
class TestAirportOperations(unittest.TestCase):

    def setUp(self):
        # Only set up what's needed by most tests
        self.airport = Airport("KAMA", "Test")

    def test_add_first_runway(self):
        self.airport.add_runway("04/22", 13502)
        self.assertEqual(len(self.airport.runways), 1)

    def test_add_second_runway(self):
        # Extend setUp for this specific test
        self.airport.add_runway("04/22", 13502)
        self.airport.add_runway("13/31", 7898)
        self.assertEqual(len(self.airport.runways), 2)
```

### 7. Test Edge Cases

```python
class TestLongestRunway(unittest.TestCase):

    def test_no_runways_returns_zero(self):
        airport = Airport("KAMA", "Test")
        self.assertEqual(airport.longest_runway, 0)

    def test_one_runway_returns_its_length(self):
        airport = Airport("KAMA", "Test")
        airport.add_runway("04/22", 13502)
        self.assertEqual(airport.longest_runway, 13502)

    def test_multiple_runways_returns_longest(self):
        airport = Airport("KAMA", "Test")
        airport.add_runway("04/22", 13502)
        airport.add_runway("13/31", 7898)
        self.assertEqual(airport.longest_runway, 13502)
```

---

## Further Reading

- [unittest documentation](https://docs.python.org/3/library/unittest.html)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Testing Python Applications with pytest](https://docs.pytest.org/) (alternative framework)
- [Test-Driven Development with Python](https://www.obeythetestinggoat.com/)
