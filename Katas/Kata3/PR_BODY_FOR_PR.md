PR: Add mocked tests for Kata3

This PR adds:
- Mock-based unit tests using `unittest.mock` and `responses`.
- Guards `kata3_api_consumer` runtime behind `main()` to avoid side effects during import.
- `README.md` documenting test approach and why mocking is used.

Files changed:
- Katas/Kata3/src/kata3_api_consumer.py
- Katas/Kata3/tests/test_api_consumer_mocked.py
- Katas/Kata3/tests/test_api_consumer_with_responses.py
- Katas/Kata3/README.md
