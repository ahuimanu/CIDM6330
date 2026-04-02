# ADR-003: Implement the MVP with the Python Standard Library

## Status

Accepted

## Context

The MVP needs acquisition, transformation, serialization, reporting, and automated tests. There were several implementation technology paths available:

- Use a third-party FRED client library plus data-analysis packages such as pandas
- Use requests-based HTTP code with additional testing helpers
- Use only the Python standard library for networking, JSON handling, file output, and unit testing

Third-party tools can reduce code volume, but they also increase environment setup, dependency management, version drift, and grading friction. Because the course emphasizes runnable software, trade-off reasoning, and explainability over framework sophistication, dependency minimization matters.

## Decision

Implement the Foundation 4 MVP primarily with the Python standard library: `urllib` for HTTP access, `json` for serialization, and `unittest` plus `unittest.mock` for automated tests. This choice favors reproducibility and low setup burden over convenience libraries.

## Consequences

Positive:

- Minimal installation burden for reviewers
- Fewer dependency/version conflicts
- Easier to explain exactly how acquisition, transformation, and testing work
- Good fit for an educational MVP whose scope is intentionally controlled

Negative:

- More manual code for HTTP handling and data manipulation
- Less ergonomic than pandas for time-series analysis
- Fewer built-in conveniences for richer live API workflows
