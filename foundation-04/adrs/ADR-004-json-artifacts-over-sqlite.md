# ADR-004: Use JSON Artifacts Instead of SQLite for the Delivered MVP

## Status

Accepted

## Context

The Foundation 2 design allowed CSV and/or SQLite persistence. Earlier experimentation showed that a local database would be useful for querying, but the delivered Foundation 4 MVP still needed to prioritize inspectability, repeatable execution, and low setup burden.

Alternatives considered in context:

- Persist transformed data in SQLite
- Persist transformed data in CSV only
- Persist raw and transformed artifacts in JSON and summarize results in markdown

SQLite would improve queryability, but it adds another artifact type, schema management, and more explanation overhead during grading. CSV is simpler, but JSON better preserves the source structure of FRED-style payloads and makes nested metadata easier to keep when needed.

## Decision

Persist the raw acquisition payload and transformed analytical dataset as JSON files, and generate a markdown summary report for human-readable output. This is the best fit for the delivered MVP because it keeps the system transparent and easy to verify while still providing durable artifacts for review.

## Consequences

Positive:

- Reviewers can inspect outputs without database tooling
- Raw payload structure is preserved naturally
- The project remains simple to run in constrained environments
- File artifacts work well with versioned coursework submission

Negative:

- Querying and comparison workflows are weaker than they would be in SQLite
- No indexed access for larger datasets
- Future analytical expansion may require migrating to a more query-friendly store
