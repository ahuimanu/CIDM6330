# AI Coding Agent Instructions - CIDM 6330

## Project Overview
Educational repository for CIDM 6330 (Software Systems Development) containing:
- **Testing examples** (`Testing/`): unittest and pytest patterns with Hillard exercises and PyTesting demos
- **Tutorials** (`tutorials/`): Self-contained examples of Python fundamentals (OOP, file handling, SQLite, HTTP, concurrency)
- **Docs** (`docs/`): Course materials on software architecture concepts

## Tooling & Environment
**Python Ecosystem**: Astral tools (uv, ruff, pyright)
- Create/activate venv: `uv venv && source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows)
- Install deps: `uv pip install -r requirements.txt`
- Lint/format: `ruff check/format --fix [file]`
- Type check: `pyright [file]`

**Target Python**: >=3.13 (pyproject.toml specifies py312 as Ruff target)

## Code Patterns & Conventions

### Type Hints & Protocols
Use Protocol-based structural typing over abstract base classes for flexibility:
```python
@runtime_checkable
class Summarizable(Protocol):
    def get_summary(self) -> str: ...
```
See [tutorials/PythonOOP/pyoop.py](tutorials/PythonOOP/pyoop.py) for examples.

### Immutable Data
Prefer frozen dataclasses for value objects:
```python
@dataclass(frozen=True)
class Location:
    city: str
    country: str
```

### Testing Framework
- **unittest**: For integration tests (Hillard examples)
- **pytest**: For unit tests with fixtures (PyTesting folder uses conftest.py)
- Pattern: Create test files alongside implementation files (e.g., `cart.py` + `test_cart.py`)

### Domain Model
Examples use consistent weather/airport domain (see tutorials and pyoop.py):
- Airports, Heliports, weather reports, locations
- Illustrates inheritance, protocols, and composition patterns

## File Organization Guidelines

**Tutorials Structure**: Each tutorial is self-contained
```
tutorials/tutorial_name/
├── tutorial_name_README.md    # Comprehensive guide with examples
└── tutorial_name_example.py   # Runnable demo
```
Run examples: `python tutorial_name/tutorial_name_example.py`

**Testing Structure**: Mirrors source code with test_ prefix
```
Testing/
├── About/                     # Generalized testing concepts
├── Hillard/                   # Dan Hillard's "Practices of Python Pro"
└── PyTesting/                 # Pytest framework examples
```

## Development Workflows

### Running Tests
```bash
# Pytest
pytest Testing/PyTesting/

# Unittest
python -m unittest Testing/Hillard/test_cart.py -v
```

### Running Tutorials
Each tutorial is executable standalone. Example:
```bash
python tutorials/sqlite/sqlite_example.py
```

## Cross-Component Communication
This is primarily an educational repo - minimal inter-component dependencies. Each tutorial and example is largely independent. Focus on:
- Clear imports and module organization
- Docstrings explaining patterns (see pyoop.py module docstring)
- Self-contained examples demonstrating concepts

## Common Issues & Patterns
- **Type checking**: Ruff respects type hints from dataclasses; use `frozen=True` for immutable objects
- **Imports**: Tutorials use stdlib first; requests/channels are in requirements.txt for specific examples
- **Comments**: Use section headers (=============) for major blocks in complex files
