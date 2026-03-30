Kata 8 — Test Doubles and Isolation
Foundation 4, Sprint Week 2

Python Focus: Testing (mocking and isolation)
Git Focus: Cherry-pick
The Exercise:

Take your Kata 3 (API client) code and add tests that don't require network access:

Mock the HTTP responses using unittest.mock or pytest-mock
Test success cases with mocked valid responses
Test error handling with mocked error responses (4xx, 5xx, timeout)
Test retry logic by mocking sequential failures then success
Requirements:

No actual network calls in tests (tests must work offline)
Use @patch or mocker fixture appropriately
Test both the happy path and edge cases
Verify that your mocks are actually being used (test would fail if real network called)
Git Tasks:

Create a branch with several commits, including one good commit mixed with experimental ones
Use git cherry-pick to bring just the one good commit to another branch:
git checkout main
git cherry-pick <commit-hash>
Understand when cherry-pick is appropriate vs. merge
Stretch:

Use responses or httpretty library for more ergonomic HTTP mocking