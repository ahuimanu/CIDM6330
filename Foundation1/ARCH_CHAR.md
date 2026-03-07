# Architecture Characteristics Discovery

## Candidate Characteristics
1.  **Auditability:** Because financial decisions are made on this data, the system must be able to prove exactly what data was available at any specific timestamp (Point-in-Time).
2.  **Scalability (Read):** Economic researchers often pull decades of data at once. The system must handle high-volume analytical queries without degrading.
3.  **Reliability:** The FRED API has rate limits (1,000 queries per minute). The architecture must reliably handle these constraints through caching or local mirroring.
4.  **Agility:** New economic series are added to FRED daily. The internal data model must be flexible enough to ingest new types of series without schema migrations.
5.  **Data Integrity:** Managing the units (e.g., "Billions of Dollars" vs. "Percent Change") is critical. Miscalculating a unit across joins would break the entire system's logic.

## Tensions & Trade-offs
* **Consistency vs. Performance:** Storing every historical revision of every data point (High Consistency/Auditability) will significantly increase storage costs and potentially slow down query performance.
* **Flexibility vs. Complexity:** Building a generic "Series Ingester" that handles any FRED ID is highly flexible but adds significant complexity to the validation logic compared to a hard-coded pipeline for just CPI and GDP.

## What I Don't Know Yet
I cannot yet assess **Deployment** or **Cost** characteristics until I decide if this system will provide real-time dashboards (high compute) or weekly PDF reports (low compute).

## FSA Mapping & Concrete Scenarios
Below are explicit mappings to Foundation of Software Architecture (FSA) quality-attribute vocabulary with short, testable scenarios.

- **Auditability (Point-in-Time Reproducibility):** Given a data-driven recommendation produced on 2026-02-01, the system can reproduce the exact input series and the derived feature values used to make that recommendation within 5 minutes of retrieval.
- **Availability (Batch Availability):** The monthly batch pipeline must complete within a 2-hour window with retries; failures must trigger alerts and preserve partial outputs for diagnosis.
- **Performance (Analytical Read Throughput):** Analytical queries over 50 years of monthly observations (≈600 rows × 6 series) should return combined CSVs in under 30 seconds on a developer laptop.
- **Modifiability / Extensibility:** Adding one new FRED series and wiring it into the pipeline should require no schema migration and be achievable with a single configuration change plus one unit test.
- **Observability / Audit Trail:** Every transformed CSV must include metadata header lines (series id, retrieval timestamp, API revision token) and a manifest file capturing which commit and `.env` (redacted) were used to produce it.
