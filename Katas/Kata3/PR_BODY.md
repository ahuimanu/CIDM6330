PR: Add mocked tests for Kata3

This PR adds:
- Mock-based unit tests using `unittest.mock` and `responses`.
- Guards `kata3_api_consumer` runtime behind `main()` to avoid side effects during import.
- `README.md` documenting test approach and why mocking is used.
