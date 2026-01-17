# Python Fundamentals Tutorials

Supplemental tutorials for CIDM 6330 covering practical Python operations that complement the OOP foundations. Each tutorial includes a comprehensive README and a runnable example file using a consistent weather/airport domain model.

## Tutorials

| Folder | Topic | Description |
|--------|-------|-------------|
| [file_handling](file_handling/) | File Handling & Serialization | pathlib, text/CSV/JSON/YAML, serialization patterns, context managers |
| [sqlite](sqlite/) | Database Operations | sqlite3, CRUD, transactions, Repository pattern, Unit of Work |
| [http_apis](http_apis/) | HTTP & Web APIs | urllib → requests → httpx progression, async HTTP, error handling |
| [concurrency](concurrency/) | Concurrency Fundamentals | threading, multiprocessing, concurrent.futures, asyncio |
| [testing](testing/) | Testing & Mocking | unittest, assertions, fixtures, mocking with unittest.mock |

## Structure

Each tutorial folder contains:

```
tutorial_name/
├── tutorial_name_README.md    # Comprehensive guide with examples
└── tutorial_name_example.py   # Runnable demonstration
```

## Running the Examples

```bash
# File Handling
python file_handling/file_handling_example.py

# SQLite
python sqlite/sqlite_example.py

# HTTP APIs (includes mock server, works offline)
python http_apis/http_apis_example.py

# Concurrency
python concurrency/concurrency_example.py

# Testing
python testing/testing_example.py
# Or with unittest verbosity:
python -m unittest testing/testing_example.py -v
```

## Dependencies

Most tutorials use only the standard library. Optional dependencies:

| Tutorial | Optional Packages | Install |
|----------|-------------------|---------|
| file_handling | PyYAML | `uv add pyyaml` |
| http_apis | requests, httpx | `uv add requests httpx` |

## Domain Model

All tutorials use a consistent weather/airport domain for continuity:

- **Airport**: Station ID, name, city, state, runways
- **Runway**: Identifier, length, surface
- **WeatherReport**: METAR, TAF, timestamp

This allows concepts to build on each other and demonstrates how the same domain objects persist, communicate over HTTP, process concurrently, and get tested.

## Connection to Course Material

These tutorials support the software architecture concepts in FSA 2nd Edition:

| Tutorial | Supports |
|----------|----------|
| File Handling | Data serialization for service communication |
| SQLite | Data access patterns, Repository pattern |
| HTTP APIs | Service-based and microservices architectures |
| Concurrency | Event-driven and distributed systems |
| Testing | Quality attributes, maintainability |

## Python Tooling

This course uses [Astral](https://astral.sh/) tools:

- **uv** - Package and environment management
- **ruff** - Linting and formatting
- **ty** - Type checking

```bash
# Create environment and install dependencies
uv venv
uv pip install -r requirements.txt

# Lint and format
ruff check .
ruff format .

# Type check
ty .
```
