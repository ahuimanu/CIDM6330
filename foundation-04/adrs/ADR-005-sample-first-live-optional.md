# ADR-005: Default to Sample Data with Optional Live FRED Retrieval

## Status

Accepted

## Context

The lecturer requires working software. At the same time, the project domain is genuinely tied to FRED data. A live-only design would be realistic, but it would also make the submission dependent on network access, API keys, rate limits, and external service availability at grading time.

Alternatives considered in context:

- Require live FRED API access for every run
- Use sample data only and remove live capability entirely
- Default to sample mode, but allow live mode when the environment supports it

Live-only would maximize realism but weaken reproducibility. Sample-only would maximize reproducibility but reduce the authenticity of the data-source decision. The middle path addresses both concerns.

## Decision

Default the MVP to sample data and keep live FRED retrieval as an optional mode controlled by environment variables. Add retry/backoff and fallback behavior so live mode degrades gracefully instead of making the entire system non-runnable.

## Consequences

Positive:

- The MVP is dependable for grading and testing
- The architecture still demonstrates a realistic external API boundary
- Offline automated tests remain deterministic
- Live retrieval can be demonstrated when credentials and connectivity are available

Negative:

- Two acquisition paths must be understood and maintained
- Sample data can hide some real-world data variability
- Users may mistake the default demo run for full live-system behavior unless the mode is documented clearly
