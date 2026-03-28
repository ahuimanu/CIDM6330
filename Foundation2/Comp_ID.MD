# Component Identification

## Component Inventory

### Ingestion Component (Data Fetcher): 
    * Responsibility: Connects to the FRED API, authenticates, and retrieves the raw time-series data for the four metrics. Handles missing data (NaN dropping). — Implemented by: `Foundation3/acquire.py`, `Foundation1/FRED_fetch.py`; helper: `Foundation1/FRED_helper.py`
    * Primary Data: Raw Index Points, Raw Percentages, and Millions of Dollars (JSON format).

### Normalization Component:
    * Responsibility: Converts all raw, mismatched units into a unified mathematical format by calculating the Month-over-Month Percent Change ($\Delta$). — Implemented by: `Foundation3/transform.py` (uses `pct_change()`)
    * Primary Data: Unsmoothed MoM Percentages.

### Aggregation Component:
    * Responsibility: Smooths the volatile MoM percentages by calculating a 3-month rolling average to identify true macroeconomic trends. — Implemented by: `Foundation3/transform.py` (uses `rolling(3).mean()`)
    * Primary Data: Smoothed Trend Percentages.

### Calculation Component (Logic Engine):
    *Responsibility: Executes the core business logic using the weighted formula $S = w_1(\Delta IP) + w_2(\Delta CapUtil) - w_3(\Delta PPI) + w_4(\Delta Inv)$. — Implemented by: `Foundation3/transform.py` (computes `S_score`)
    * Primary Data: The calculated Supply Health Score ($S$).

### Enrichment & Output Component:
    * Responsibility: Evaluates the $S$ score against predefined thresholds to generate the final business recommendation and formats the output. — Implemented by: `Foundation3/transform.py` (adds `Recommendation`) and `Foundation3/pipeline.py` (writes `transformed.json`)
    * Primary Data: The final actionable JSON payload containing the "OVERBUY" or "HOLD" boolean.

## Partitioning approach

    *Technical Partitioning- The Shortage Scout is a Pipeline architecture. So components are inherently separated by their technical responsibility (fetching, transforming, calculating) rather than by domain. It is not creating separate "Inventory" and "Production" components (Domain Partitioning) because all four economic variables must flow together through the exact same technical transformations to produce a single mathematical result. Structuring by technical workflow perfectly matches the sequential nature of a data pipeline.

## Boundaries

    *Component Boundaries: > The boundaries between components are strictly defined by the data contracts (the "pipes") passed between them. A component boundary ends the moment it hands off a fully transformed data payload (e.g., a Pandas DataFrame) to the next sequential step. The components do not share internal state; they only know what they receive as input and what they must produce as output.

    * Cohesion Type: Functional Cohesion
    Every component in this design exhibits Functional Cohesion, each component is responsible for doing exactly one well-defined task. The Normalization Component only normalizes; it does not fetch data, and it does not calculate the final score. This strict functional cohesion is what allows the system to achieve its critical driving characteristic of Testability.