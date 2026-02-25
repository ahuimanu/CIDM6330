# Data sources: Which specific datasets, tables, or API endpoints will you use? (This should refine your Foundation 1 selection.)
## Primary API Endpoint: 
    * FRED REST API (/series/observations)

## Ingested Series:

    * IPG3344S: Industrial Production for Semiconductors (The primary volume indicator)

    * CAPUTLG3344SQ: Capacity Utilization for Semiconductors (The system stress test)

    * A34STI: Manufacturer Inventories: Computers and Electronics (The buffer check)

    * PCU334413334413: Producer Price Index for Semiconductors (The upstream pricing signal)

# Data relationships: How do these sources connect? What joins or correlations are required?
    *The four distinct time-series datasets will be fetched independently from the FRED API and merged using a full outer join on the date attribute acting as the primary key. This aligns the disparate economic indicators into a single chronological row per month.

# Transformation requirements: What must happen to the data between source and use? Aggregation? Filtering? Enrichment? Calculation?

## Filtering(Handling Missing Data)
    * Because the Federal Reserve updates different datasets on different days (e.g., Production might update on the 15th, but Inventories on the 20th), an outer join by date will leave empty gaps (NaN values) for the most recent month. The pipeline must filter out these incomplete rows so the system doesn't accidentally trigger a multi-million dollar "Overbuy" recommendation based on half-missing data.

## Calculation (Unit Normalization)
    * Units differ between datasets (Millions of dollars vs. Index vs. Percentage) and will need to calculate to percentage change month-over-month for every column. This calculates the growth rate enabling normalization across all four datasets.

## Calculation(The Logic Gate)
    *Once the units are normalized into percentages, the pipeline performs the core architectural calculation: executing your weighted formula to derive the final monthly score.

## Enrichment (Business Value)
    *The final step is to enrich the data row by appending a plain-text boolean column (e.g., Recommendation). The pipeline logic evaluates the $S$ score against a defined threshold and enriches the output with either "OVERBUY" or "HOLD".
    
# Output shape: What does the processed data look like? What will downstream consumers (users, reports, APIs, models) receive?
    *The pipeline will output a structured JSON payload (or a finalized database row) for each monthly time-series entry. To satisfy the strict Auditability characteristic, the output will include not only the final recommendation but also the point-in-time raw data and the intermediate calculations.The payload will include:
        **Timestamp: The exact date of the economic observation.
        **Raw Ingests: The raw values for IPG3344S, CAPUTLG3344SQ, A34STI, and PCU334413334413.
        **Transformed Metrics: The 3-month rolling average of the percent changes for each variable.
        **The Core Metric: The final calculated Supply Health Score ($S$).
        **The Enriched Output: A boolean/string Recommendation field (e.g., "OVERBUY" or "HOLD").