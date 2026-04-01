# AI Collaboration Log - Kata 8 (Test Doubles and Isolation)

## Context
This assignment extended the Kata 3 FRED API client by adding isolated tests that do not require internet access and by documenting a cherry-pick workflow for the Git portion of the assignment.

## AI Tools Used
- ChatGPT for testing strategy, mocking guidance, and submission wording
- OpenAI Codex for code inspection, test implementation, branch workflow, and verification

## Interaction 1 - Identifying Kata 3 Reuse

**What I asked:**
I asked whether my existing Kata 3 API client could be used as the basis for Kata 8.

**What AI provided:**
- It located the Kata 3 API client functions responsible for HTTP requests, retries, pagination, and output writing.
- It identified `request_with_backoff` and `fetch_all_observations` as the best targets for isolated tests.

**What I used:**
- I reused the Kata 3 API client as the implementation under test.

## Interaction 2 - Designing Offline Tests

**What I asked:**
I asked how to test HTTP behavior without making real network calls.

**What AI provided:**
- Guidance on using `unittest.mock.patch` to replace `requests.get`
- Suggestions for mocked success responses, HTTP failures, timeouts, and sequential retry scenarios
- A recommendation to mock `time.sleep` and jitter behavior so retry tests stay fast and deterministic

**What I used:**
- Patched `requests.get`, `time.sleep`, and `random.uniform`
- Added tests for success, 4xx, 5xx, timeout, retry, pagination, and output writing

## Interaction 3 - Verifying Isolation

**What I asked:**
I asked how to prove that the tests would fail if a real network call slipped through.

**What AI provided:**
- A guard-style test that patches `requests.get` to raise immediately if used unexpectedly

**What I used:**
- A dedicated test that confirms mocks are active and that real network access is not required

## Interaction 4 - Git Cherry-pick Workflow

**What I asked:**
I asked how to satisfy the Git portion of the assignment involving cherry-pick.

**What AI provided:**
- A workflow using a branch with mixed commits and a clean submission branch created via `git cherry-pick`
- A clear explanation of when cherry-pick is more appropriate than merge

**What I used:**
- I prepared the submission workflow around a cherry-picked good commit for the final branch

## Where AI Was Limited or Incorrect
- AI could suggest testing structures, but local verification was still required to ensure imports, paths, and commands matched the repo layout.
- The final submission branch still needed manual validation through git and test commands.

## Key Takeaways
- Mocking makes API tests fast, deterministic, and independent of network conditions.
- Retry logic is much easier to verify when sleeps and randomness are patched.
- Cherry-pick is useful when only one commit from a messy branch should appear in the final submission branch.

## Reflection
AI helped speed up the implementation and verification of the Kata 8 test suite, but I still needed to validate that the mocks, branch workflow, and final commands matched the actual repository structure and assignment rubric.
