Python Focus: Testing (pytest basics)
Git Focus: Pre-commit Hooks
The Exercise:

Take your Kata 2 (SQLite module) or Kata 4 (pipeline) code and add comprehensive tests:

Unit tests for individual functions
Fixture setup for database state
Parameterized tests for multiple input scenarios
Tests for error conditions (what happens with bad input?)
Requirements:

Use pytest (not unittest)
Use fixtures for setup/teardown
Use pytest.mark.parametrize for at least one test
Achieve meaningful coverage of your core logic (use pytest-cov to measure)
Git Tasks:

Set up a pre-commit hook that runs your tests:
Create .git/hooks/pre-commit
Make it executable
Have it run pytest and block commit if tests fail
Attempt a commit with failing tests, observe the block
Fix tests, commit successfully
Stretch:

Add a hook that also runs ruff or flake8 for linting