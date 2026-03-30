**Tests and Mocking**

- **What**: This folder includes unit tests for `fetch_fred_data_with_retry` that run offline using mocks.
- **Why**: Tests should be deterministic, fast, and not depend on external network availability. Mocking HTTP responses isolates behavior (success, 4xx, 5xx, timeouts, retry sequences) so tests validate logic rather than the network.
- **How**: Two styles are used:
  - `unittest.mock` (`tests/test_api_consumer_mocked.py`) to patch `requests.get` and `time.sleep` for fast, focused unit tests.
  - `responses` (`tests/test_api_consumer_with_responses.py`) to declaratively mock HTTP endpoints and response sequences as an ergonomic alternative.
- **Run tests** (from repo root, in the project venv):

```bash
.venv/Scripts/python.exe -m pytest Katas/Kata3/tests -q
```

- **Learning notes**: Mocking is essential for isolation. The tests here exercise both happy-path and error-handling paths (including retry logic), which helps build confidence in production behavior without hitting the real API.
