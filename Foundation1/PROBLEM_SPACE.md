# Initial Problem Space: Hardware OEM Strategic Decision Support

## Domain Observations: The "Hardware Lag"
In the hardware industry (Dell, HP, Lenovo), decisions made today regarding component procurement and factory allocation won't hit the market for 3–6 months. Exploring FRED data reveals that economic shifts (like Interest Rate hikes or Semiconductor production dips) act as "early warning signals" before they show up in company quarterly earnings. I noticed that while Consumer Sentiment (`UMCSENT`) is volatile month-to-month, the Producer Price Index (`PCU334111334111`) shows much stickier, long-term trends that directly impact profit margins.

## Candidate Problems (The Manager's Dashboard)

### 1. The "Margin Protector" (Pricing Strategy)
* **Business Problem:** How can we protect margins when the "Cost to Build" spikes?
* **Data Logic:** Monitor PPI for Electronic Computer Manufacturing. If component costs trend up by >5% over two quarters while MSRP remains flat, margins are at risk.
* **Architectural Goal:** Build a "Price-to-Cost" correlation engine that suggests MSRP adjustments or triggers supplier contract renegotiations.

### 2. The "Capital Cost" Forecast (Enterprise Refresh Cycles)
* **Business Problem:** Will Fortune 500 clients delay their 3-year laptop refresh due to high interest rates?
* **Data Logic:** Correlate the `FEDFUNDS` rate with enterprise sales cycles. High rates increase the "Cost of Capital," leading CFOs to "sweat the assets" (make old laptops last longer).
* **Architectural Goal:** A predictive model that advises the sales team to pivot from "New Hardware Sales" to "High-Margin Support Services" when rates exceed a specific threshold.

### 3. Supply Chain "Shortage Scout"
* **Business Problem:** How do we avoid "Out of Stock" notices during semiconductor dips?
* **Data Logic:** Use Industrial Production of Semiconductors (`IPG3344S`) as a 3-to-6 month leading indicator for hardware availability.
* **Architectural Goal:** A stockpiling logic gate. If chip production dips, the system recommends "overbuying" inventory to ensure Dell/HP has stock while competitors run dry.

### 4. The "Tier Shifter" (Product Mix Optimization)
* **Business Problem:** Should we manufacture more budget units (Inspiron) or premium workstations (XPS)?
* **Data Logic:** Track Consumer Sentiment (`UMCSENT`) and Disposable Income (`DSPIC96`). Cratering sentiment indicates consumers will "trade down" to entry-level units.
* **Architectural Goal:** A factory-reallocation recommender that adjusts the "Production Mix" ratio based on the health of the consumer.

## Questions I Can't Yet Answer
* **Weighting:** Which indicator is the *most* predictive? Does Consumer Sentiment matter more than Interest Rates for a company that is 70% Enterprise focused?
* **External Factors:** How do I architect for "Black Swan" events (like a port strike or a specific factory fire) that FRED data won't capture?
* **Granularity:** FRED gives national data, but Dell sells globally. How much "noise" is introduced by using US economic data to predict global supply chain movements?