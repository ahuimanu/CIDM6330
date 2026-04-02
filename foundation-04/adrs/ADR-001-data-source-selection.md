# ADR-001: Use FRED Real GDP (GDPC1) as the Primary Dataset

## Status

Accepted

## Context

The Foundation 2 problem statement committed to a system that monitors U.S. economic growth and identifies potential downturn signals using GDP trends. That requires a source with an authoritative macroeconomic time series, clear documentation, stable identifiers, and enough historical depth to support quarter-over-quarter and year-over-year calculations.

Alternatives considered in context:

- Generic GDP-like sample files only
- Other approved government datasets that would require joining multiple series before producing a basic growth-monitoring MVP
- A broader multi-indicator design using several FRED series at once

Those options were weaker for this MVP. Sample data alone is good for repeatability but weak for problem legitimacy. Multi-source or multi-series scope would increase complexity before the single-series analytical pipeline was proven.

## Decision

Use FRED Real GDP as the primary dataset, with the project centered on GDP/FRED observations and the implementation retaining compatibility with live FRED retrieval. This best addresses the course problem because it gives a documented government-adjacent economic source, a time-series shape that naturally fits pipeline processing, and a direct path to the trend indicators promised in Foundation 2.

## Consequences

Positive:

- Strong fit with the original problem definition
- Natural support for time-ordered analysis such as QoQ and YoY comparisons
- Clear architectural story around repeatability, API access, and time-series transformation
- Good continuity across Foundations 1 through 4 because the same domain and dataset family are preserved

Negative:

- The MVP remains single-series and therefore does not address richer cross-indicator analysis
- Live retrieval introduces external dependency risk, rate limits, and credential management concerns
- GDP is updated relatively slowly compared with higher-frequency economic indicators, so some "real-time" behavior is limited
