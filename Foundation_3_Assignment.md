# Talent Sentinel 

This project implements a data-driven "Command Center" to address the **retention blind spot** in public sector management. By integrating **Texas State JOLTS** data with **National JOLTS** macroeconomic signals, the pipeline identifies if high turnover is a localized issue or a reflection of broader "Market Heat".

---

## 1. MVP Iteration 1 - Data Acquisition
The system reliably acquires macroeconomic data via the Bureau of Labor Statistics (BLS) Public API.

* **Working Code**: `fetch_bls.py` handles the connection to the BLS API using `requests.post`.
* **Data Samples**: Produces a raw JSON response from BLS containing monthly data for Hires, Quits, and Openings for both Texas (`JTU48...`) and National (`JTU00...`) series.
* **Error Handling**: Implements a 3-attempt retry loop with exponential backoff to handle rate limits and network timeouts. It specifically catches `429` (Rate Limit) and `500` (Server Error) status codes.
* **Documentation**: Detailed inline comments and a structured `config.py` allow users to swap API keys or Series IDs effortlessly.

---

## 2. MVP Iteration 2 - Data Transformation
The pipeline transforms raw, nested JSON into a structured analytical format tailored for flight risk detection.

* **Working Code**: `transform_bls.py` utilizes `pandas` to pivot raw series data into a unified monthly dataframe.
* **Transformation Logic**:
    * Calculates the **Market Heat Index** ($Openings / Hires$) to measure private-sector competition.
    * Calculates **Relative Turnover Propensity (RTP)**: $(Local\ Quit\ Rate - National\ Quit\ Rate) \times Market\ Heat$.
* **Data Quality Handling**: Uses `pd.to_numeric(errors='coerce')` to handle malformed strings and `dropna()` to ensure only complete monthly records are analyzed.
* **Output Artifacts**: Produces `bls_monthly.csv`, a cleaned dataset ready for merging and visualization.

---

## 3. MVP Iteration 3 - Pipeline Integration
A coherent, end-to-end flow from BLS source to validated risk alerts.

* **Working Pipeline**: `run_pipeline.py` chains the entire process: `Fetch → Transform → Combine → Validate`.
* **Configuration**: Managed via `config.py`, allowing users to set `START_YEAR`, `END_YEAR`, and `BLS_API_KEY` without modifying logic.
* **Logging**: `common.py` initializes a centralized logger that records progress and errors to both the console and a persistent log file.
* **Output Demonstration**: The pipeline produces `talent_radar_final.csv`, which labels each month with a Risk Quadrant (e.g., "Internal Crisis" or "Safe Zone").



---

## 4. Architecture Reality Check
Implementation revealed that real-world data is far noisier than initial designs suggested.

* **Style Validation**: The **Modular ETL** style remains effective, but the "Micro" (Austin) data was too sparse, requiring a pivot to **State-Level JOLTS** for a true monthly radar.
* **Characteristic Assessment**:
    * **Observability**: Achieved via structured logging, making failures easy to trace.
    * **Fault Tolerance**: Harder than expected; the BLS API often returns "Success" status even when internal data is missing, requiring secondary validation.
* **Component Evolution**: Boundaries shifted; the `transform` layer now carries more responsibility for metric calculation (RTP) to keep the `combine` layer lightweight.
* **Lessons Learned**: Dependency on municipal open data portals is risky, as they often lack the update frequency required for real-time systems.

---

## 5. Distributed Considerations
The current pipeline is a **functional monolith**.

* **Defense of Non-Distribution**: Given the low volume of BLS data, a distributed system would introduce unnecessary network overhead and complexity.
* **Trade-offs**: Distributing would gain horizontal scalability for multi-state analysis but lose the simplicity of local state management.
* **Data Ownership**: Truth lives in the `RAW_DIR` (as immutable JSON). Downstream components "borrow" this data but never modify the original source.

---

## 6. Risk Identification
Identifying the "weak links" in the current implementation.

* **Technical Risks**: Concentrated in the `fetch_bls.py` module; if the BLS API schema changes, the parsing logic may break.
* **Data Risks**: The primary risk is **Seasonality Noise**. Comparing unadjusted state data to adjusted national data can create "false positive" alerts.
* **Architectural Risks**: The system assumes a linear relationship between $Openings$ and $Hires$; disruption of these ratios would require significant rework of RTP thresholds.