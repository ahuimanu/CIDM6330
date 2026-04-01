# AI Collaboration Log — Kata 7 (Unit Testing Fundamentals)

## Context
This assignment involved adding pytest-based unit tests to the SQLite module from Kata 2, along with setting up a pre-commit hook for automated testing and linting.

---

## AI Tools Used
- ChatGPT (for guidance, debugging, and workflow clarification)
- OpenAI Codex (via VS Code) for code inspection and suggestions

---

## Interaction 1 — Code Analysis (Codex)

**What I asked:**
I asked Codex to inspect my Kata 2 SQLite module and identify any issues before writing tests.

**What AI provided:**
Codex identified several important issues:
- Foreign keys not enforced in SQLite
- Lack of UNIQUE constraint on observations
- Undefined behavior for deletes
- Potential issues with date validation
- Ambiguity in aggregate query logic

**What I used:**
- Enabled `PRAGMA foreign_keys = ON` in the connection setup

**What I modified/rejected:**
- Did not implement all schema changes (e.g., UNIQUE constraint) because they were outside the assignment scope

**Why:**
Focused on testability and assignment requirements rather than redesigning the schema

---

## Interaction 2 — Test Design (ChatGPT)

**What I asked:**
How to structure pytest tests with fixtures, parameterization, and error handling

**What AI provided:**
- Suggested using `tmp_path` for isolated databases
- Recommended fixture-based setup
- Provided guidance on parameterized tests and edge cases

**What I used:**
- Fixtures for database setup and seeding
- `pytest.mark.parametrize` for multiple input scenarios
- Error-condition tests using `pytest.raises`

**What I modified:**
- Adjusted test cases to match actual behavior of my SQLite implementation

---

## Interaction 3 — Debugging Failing Test

**Issue:**
A test expecting `IntegrityError` did not fail when inserting `None` values

**What I asked:**
Why SQLite was not raising errors for NULL values

**What AI explained:**
- SQLite only enforces constraints explicitly defined (e.g., NOT NULL)

**What I did:**
- Aligned test expectations with current schema behavior

---

## Interaction 4 — Pre-commit Hook Setup

**What I asked:**
How to create a pre-commit hook that runs pytest

**What AI provided:**
- Steps to create `.git/hooks/pre-commit`
- Script to run pytest and block commits

**What I used:**
- Implemented hook that runs pytest before commit
- Verified commit blocking when tests failed

---

## Interaction 5 — Stretch Goal (Linting)

**What I asked:**
How to extend the hook to include linting

**What AI provided:**
- Suggested using Ruff

**What I used:**
- Added Ruff to pre-commit hook

**Issue encountered:**
- Lint failure due to unused import

**Resolution:**
- Removed unused import (`Iterable`)

---

## Interaction 6 — Git Workflow Recovery

**Issue:**
My GitHub fork was deleted due to loss of collaborator access

**What I asked:**
How to recover and continue submission workflow

**What AI provided:**
- Recommended creating a new personal repository
- Guided reconnection of local repo using `git remote set-url`

**What I did:**
- Created new repo under my account
- Repointed origin
- Successfully pushed branch

---

## Where AI Was Limited or Incorrect

- Codex suggested schema improvements that were outside assignment scope
- AI did not fully account for SQLite’s default constraint behavior initially
- Some debugging required manual verification beyond AI suggestions

---

## Key Takeaways

- AI is useful for analysis and guidance, but implementation requires verification
- Understanding SQLite behavior is critical for writing correct tests
- Pre-commit hooks enforce discipline and improve code quality
- Git issues (like deleted forks) require manual problem-solving beyond AI suggestions

---

## Reflection

AI significantly accelerated the development of tests and debugging, but I maintained control over implementation decisions. I validated all outputs through testing and adjusted based on actual system behavior. This process improved both my technical understanding and my ability to critically evaluate AI-generated suggestions.