# Kata 8 - Test Doubles and Isolation

## Overview
This kata extends the Kata 3 API client by adding a fully offline test suite that uses test doubles to isolate network behavior.

## Requirements Checklist

### Python Focus
- No real network calls are made in tests.
- `unittest.mock.patch` is used to mock HTTP responses and timing behavior.
- Tests cover success cases, HTTP 4xx and 5xx failures, timeout handling, retry behavior, and pagination.
- A guard test proves the mocks are actually being used by failing immediately if a real network call is attempted.

### Git Focus
- A mixed-history branch was created with experimental work and one good Kata 8 commit.
- `git cherry-pick` was used to move the good commit onto a clean submission branch.
- The submission branch contains only the intended Kata 8 changes.

## Test Cases Added
- Successful mocked HTTP response returns parsed JSON
- Mocked 404 response raises runtime failure
- Sequential mocked 500 then success exercises retry logic
- Mocked timeout then success exercises retry logic
- Pagination is tested with mocked sequential payloads
- `max_pages` stopping behavior is tested offline
- Output writing is tested without network access
- A guard test fails if a real network call is attempted

## Commands
Run Kata 8 tests from the repo root:

```powershell
python -m pytest foundation-02/foundation-02/katas/kata-03-api/tests
```

Run lint checks for the Kata 8 files:

```powershell
python -m ruff check foundation-02/foundation-02/katas/kata-03-api
python -m ruff check foundation-04/kata-08
```

## Cherry-pick Notes
`git cherry-pick` is appropriate when you want to move one specific commit from one branch to another without bringing along the rest of that branch's history.

A merge is more appropriate when you want to preserve the full branch history and combine all commits from that branch.

## Verification
- Tests run fully offline because `requests.get` is mocked.
- Retry logic is exercised with sequential mocked failures followed by success.
- The submission branch was prepared by cherry-picking the good Kata 8 commit onto a clean branch.
