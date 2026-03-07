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