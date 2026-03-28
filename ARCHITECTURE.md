# Architecture Decision Record — Shortage Scout

## Context
The Shortage Scout project is a low-traffic, monthly batch pipeline that computes an `S` score from several FRED time-series to support inventory recommendations.

## Decision
We implement a Pipeline (Pipes & Filters) architecture as a single-process batch pipeline invoked via CLI. Components are: acquisition, transformation, and output. This keeps data lineage clear and simplifies testing.

## Consequences
- Pros: simple to reason about, easy to test locally, strong auditability and reproducibility for business reviewers.
- Cons: limited scalability if data volume or frequency grows; not horizontally distributed; upgrades to distributed components would require additional coordination and observability work.

## Alternatives considered
- Microservices: rejected due to added complexity for a monthly batch job.
- Serverless per-step functions: considered but increases operational surface and complexity for data consistency.
