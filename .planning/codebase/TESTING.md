---
title: Testing Patterns
mapped: 2026-05-04
---

# Testing

## Framework

- **pytest** — primary test runner
- `responses` library — HTTP API mocking
- `unittest.mock` — function/method patching

## Test File Locations

```
Foundation3/tests/
  test_acquire.py           # FRED API acquisition tests (mocked)
  test_transform.py         # Data transformation unit tests
  test_transform_weights.py # S-score weight calculation tests

Foundation1/
  lag_test.py               # Lag analysis tests

Katas/
  conftest.py               # Shared fixtures (tmp_sqlite_db)
  Kata2/test_sqlite_kata.py # SQLite ORM exercise tests
  Kata3/tests/
    test_api_consumer_mocked.py    # unittest.mock HTTP mocking
    test_api_consumer_with_responses.py  # responses library mocking
  Kata4/test_pipeline.py    # Pipeline integration tests
  Kata9/test_integration.py # Full pipeline integration (1000-row synthetic)
  Kata10/test_weather_stats.py     # Weather statistics unit tests (TDD kata)

Testing/
  Hillard/test_cart.py      # Shopping cart TDD exercise
  Hillard/test_product.py   # Product TDD exercise
  PyTesting/Tests/
    test_stack.py           # Stack data structure tests
    test_queue.py           # Queue data structure tests

tutorials/
  roman_numerals_kata/test_number_to_numeral.py
```

## Fixtures

Shared fixture in `Katas/conftest.py`:
```python
@pytest.fixture
def tmp_sqlite_db(tmp_path):
    # Creates ephemeral SQLite DB; accepts optional schema param
```

Common fixture patterns:
- `tmp_path` (pytest built-in) for file I/O tests
- `monkeypatch` for module-level attribute patching
- Custom fixtures for test data generation

## Mocking Strategies

### HTTP Mocking (two approaches)

**unittest.mock approach** (`Katas/Kata3/tests/test_api_consumer_mocked.py`):
```python
@patch("kata3_api_consumer.requests.get", return_value=resp)
@patch("kata3_api_consumer.time.sleep", lambda *_: None)
def test_fetch(mock_sleep, mock_get):
    ...
```

**responses library approach** (`Katas/Kata3/tests/test_api_consumer_with_responses.py`):
```python
@responses.activate
def test_fetch():
    responses.add(responses.GET, url, json=payload, status=200)
    ...
```

**Foundation3 approach** (monkeypatch):
```python
monkeypatch.setattr("acquire.get_fred_series_with_payload", fake_fn)
monkeypatch.chdir(tmp_path)
```

### Time Mocking
```python
@patch("module.time.sleep", lambda *_: None)  # eliminate retry delays
```

## Assertion Styles

- Standard pytest: `assert isinstance(result, pd.DataFrame)`
- Floating-point tolerance: `assert abs(avg - 2.0) < 1e-6`
- Rounded comparison: `assert round(value, 6) == round(expected, 6)`
- Exception testing: `with pytest.raises(ValueError):`
- File existence: `assert output_path.exists()`
- DataFrame shape: `assert df.shape == (expected_rows, expected_cols)`

## Test Data Philosophy

- **Synthetic data preferred** — hermetic, reproducible, no network I/O in tests
- Helper factories: `make_fred_rows(n=1000)`, `make_response(status, json)`
- Deterministic generation for statistical tests (known mean, variance)
- `@pytest.mark.parametrize` for multi-case coverage

## Test Patterns

### Arrange-Act-Assert
All tests use explicit AAA structure with comments:
```python
# Arrange
data = make_fred_rows(100)
# Act
result = transform(data)
# Assert
assert result["pct_change"].notna().all()
```

### Volume Testing
`Katas/Kata9/test_integration.py` tests with 1000-row datasets for:
- Statistical correctness (mean, standard deviation)
- Performance validation
- Idempotency (running twice gives same result)

### Edge Cases
- Empty inputs
- Malformed/missing data
- Values outside expected range

## Known Testing Gaps

- `Katas/Kata9/test_integration.py` lines 231-235: empty CSV causes `TypeError`/`AttributeError` — documented as known; pipeline hardening deferred
- Type checking not integrated into test CI pipeline yet
- Coverage not measured (`.coverage` file exists but no enforced threshold)
- Ruff pre-commit only applies to `Foundation*`; Katas not linted in CI
