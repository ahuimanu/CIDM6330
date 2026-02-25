# Problem statement: One clear paragraph describing the business problem your system will address. Be specific about who has this problem and why it matters.
Happening right now, the PC industry suffers from unpredictable part supply shortages driven by production dips, logistical congestion, and material cost spikes, causing extended lead times and eroded profit margins. To combat this, Supply Chain Managers need a robust, automated "Sense-and-Respond" system that looks beyond a single metric. By calculating a weighted Supply Health Score ($S$) that integrates FRED data across production (IPG3344S), capacity utilization (CAPUTLG3344SQ), inventories (A34STI), and pricing (PCU334413334413), this architecture will differentiate between temporary blips and systemic supply chain failures. When a falling $S$ score predicts a critical shortage, the system will trigger an "Overbuy" recommendation, empowering managers to build a data-backed business case to secure inventory and gain a decisive market advantage over competitors.

# Why this problem: From your Foundation 1 candidates, why did you select this one? What did you learn during discovery that made this the right choice?
During the discovery phase, I evaluated four candidate problems but selected the "Shortage Scout" because it offers the most robust "Sense-and-Respond" architectural challenge. While exploring the data, I discovered that consumer-focused metrics (like Sentiment) are highly volatile, whereas supply-side metrics (like Producer Prices and Industrial Production) show sticky, long-term trends. Because the hardware industry operates on a 3-to-6 month "hardware lag", building a predictive logic gate on these stable leading indicators allows the architecture to trigger high-value business actions (inventory stockpiling) with enough lead time to actually affect market outcomes, moving this system beyond a simple reporting dashboard.

# Scope boundaries: What is explicitly in scope? What is explicitly out of scope? Where are the edges of your system?
## Explicitly in Scope: 
    * Data Ingestion: Fetching monthly data from the FRED REST API for our specific indicators: Production (IPG3344S), Capacity Utilization (CAPUTLG3344SQ), Inventories (A34STI), and Pricing (PCU334413334413).
    * Logic Engine: Calculating the weighted Supply Health Score ($S$) to determine the overall health of the supply chain.
    * Recommendation Output: Generating an actionable "Overbuy" or "Hold" recommendation for the Supply Chain Manager based on the $S$ score threshold.
## Explicitly out of Scope: 
    * "Black Swan" Events: The system relies on economic trends and cannot predict sudden external shocks like port strikes, natural disasters, or factory fires.
    * Global Data Feeds: Because FRED data is US-centric, tracking international localized data is out of scope. We are using the US market as a proxy for global trends.
    * Automated Purchasing Execution: The system recommends an overbuy to a human manager; it does not integrate with a procurement system to automatically spend company money.

# Success criteria: How would you know if your system solved this problem? What would "working" look like?
## Business Success: 
    * Forecast Accuracy (Backtested): Because we cannot wait 3 to 6 months in real-time to observe a future market shortage, the system's predictive accuracy will be validated via historical backtesting. The architecture will be considered successful if it can calculate the $S$ score using only data available prior to the known 2020-2021 chip shortage, and successfully trigger an "Overbuy" recommendation before the historical shortage actually hit the market.
## Architectural Success:
    * Auditability (Point-in-Time): Because financial decisions are being made based on the FRED data, a key success metric is that the system can prove exactly what the data looked like on the day it made the recommendation
    * Reliability: The system successfully ingests monthly data from the FRED API without failing or exceeding rate limits (1,000 queries per minute)
