# Dataset Selection & Justification

## Source and Scope
* **Agency:** Federal Reserve Bank of St. Louis (FRED)
* **Dataset:** Federal Reserve Economic Data (FRED) API
* **Specific Series to be Explored:**
    1. **CPIAUCSL:** Consumer Price Index for All Urban Consumers (Inflation)
    2. **PCU334111334111:** PPI: Electronic Computer Manufacturing
    3. **FEDFUNDS:** Federal Funds Effective Rate
    4. **IPG3344S:** Industrial Production: Semiconductor & Electronic Components
    5. **UMCSENT:** University of Michigan: Consumer Sentiment
    6. **DSPIC96:** Real Disposable Personal Income

## Access Verification
I have verified access to the FRED REST API. I successfully retrieved observations for the core series using a sample `GET` request.

**Sample Data (CPI):**
date,realtime_start,realtime_end,value


1947-01-01,2026-02-08,2026-02-08,21.48


1947-02-01,2026-02-08,2026-02-08,21.62


1947-03-01,2026-02-08,2026-02-08,22.0


1947-04-01,2026-02-08,2026-02-08,22.0

## Relational Depth
This project requires joining high-frequency and mixed-domain datasets:
* **Series Join:** I will join `FEDFUNDS` (monetary policy) with `IPG3344S` (industrial output) to analyze how interest rate changes lag or lead manufacturing production.
* **Industry Cross-Reference:** Joining `PCU334111334111` (Computer PPI) with `IPG3344S` (Semiconductor Industrial Production) to model supply-chain cost pressures versus output volume.
* **Sentiment vs. Reality:** Correlating `UMCSENT` (Consumer Sentiment) with `DSPIC96` (Real Income) to identify architectural boundaries between "perceived" and "actual" economic health.

## Temporal Characteristics
* **Update Frequency:** Mostly **Monthly**, though Fed Funds data can be viewed at higher daily frequencies.
* **Historical Depth:** Most series provide data back to the **1940s or 1950s** (e.g., FEDFUNDS starts in 1954), offering massive historical depth for backtesting.
* **Granularity:** Monthly observations.

## Why This Dataset?
The inclusion of sets like **Semiconductor production** and **Consumer sentiment** creates a unique architectural challenge. It moves the project beyond a simple dashboard into a complex "Sense-and-Respond" architecture—modeling how psychological data (Sentiment) interacts with hardware supply chains (Semiconductors).