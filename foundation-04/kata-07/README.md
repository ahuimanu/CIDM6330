# Kata 7 — Unit Testing Fundamentals

## Overview
This kata extends the SQLite module from Kata 2 by adding a comprehensive pytest-based test suite and integrating a pre-commit hook to enforce test execution before commits.

## Testing Implementation

### Unit Tests
I created unit tests covering:
- station CRUD operations
- observation CRUD operations
- join query (daily summary)
- seed data functionality

### Fixtures
Fixtures were used to:
- create temporary SQLite databases using `tmp_path`
- ensure clean setup and teardown per test
- provide a seeded database state when needed

### Parameterized Tests
I used `pytest.mark.parametrize` to test:
- multiple date ranges
- edge cases in filtering logic
- repeated input scenarios

### Error Condition Testing
Tests were written to validate:
- NOT NULL constraints (name, state)
- invalid updates and deletions
- foreign key enforcement
- behavior with missing or invalid data

## Coverage
Coverage was measured using `pytest-cov`.

Command used:
```bash
py -m pytest --cov=kata2 --cov-report=term-missing