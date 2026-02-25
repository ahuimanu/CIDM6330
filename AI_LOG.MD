# AI Collaboration Log

## Foundation 1

### What I Asked
* Compare BTS, BLS, and FRED datasets.
* Refine the problem space to focus specifically on Hardware OEMs (Dell, HP, Lenovo).
* Identify business-specific FRED series for Pricing, Supply Chain, and Demand Forecasting.
* **Task:** Develop a FRED fetch script and a helper script to manage API keys and determine file types (CSV vs. JSON) for ingestion.

### What I Got
* Strategic business cases for FRED data (e.g., using `FEDFUNDS` to predict refresh cycles).
* Structured Markdown templates for Foundation 1.
* A Python helper strategy for managing the FRED API's authentication and data retrieval constraints.

### What I Used, Modified, or Rejected
* **Used:** The concept of "Leading Indicators" for supply chain risk.
* **Used:** The "Margin Protector" business case.
* **Modified:** Shifted the focus from general "Finance" to "Hardware OEM Strategy" to increase the potency of the project.
* **Added:** Specifically added a task to build a modular fetch and helper script for the data pipeline.

### My Judgment Calls
I prioritized **Interpretability** as a core architecture characteristic. Because this system is designed for business managers, the architecture cannot be a "black box"; it must provide the lineage of the data (Series ID and Revision date) for every recommendation.

## Foundation 2

### What I Asked
    *I asked the AI to help me narrow down my broad list of architecture characteristics to the top three driving forces for the "Shortage Scout" system.

    *I requested help defining strict, measurable goals for those top three characteristics (Auditability, Data Integrity, and Testability).

    *I asked for an architecture style recommendation that would physically support my mathematical pipeline.

    *I challenged the AI to evaluate alternative styles (like Microservices and Service-Based architectures) and specifically asked it to analyze the "Distributed Monolith" anti-pattern.

### What I Got
    *Problem Refinement: The AI helped filter out irrelevant operational characteristics (like Scalability and Elasticity) by reminding me this is a low-traffic, monthly batch job.

    *Corrections: It corrected my initial confusion between a Reliability failure (the system crashing) and a Data Integrity failure (the system silently outputting bad math).

    *Style Recommendation: It strongly recommended the Pipeline Architecture (Pipes and Filters) to enforce strict, sequential data transformations.

    
### What I Used, Modified, or Rejected
    *Used: I used the AI's recommendation for the Pipeline architecture and its formal definitions for Component Identification (Technical Partitioning, Functional Cohesion).

    *Modified: I modified the AI's basic rejection of Microservices by forcing an analysis of Service-Based architectures, allowing me to write a much more academically rigorous "Alternatives Considered" section.

    *Rejected: I actively rejected the need for high Reliability or distributed components. I accepted the Pipeline's trade-off that failing loudly (crashing) is significantly safer than failing silently and outputting an incorrect financial recommendation.

### My Judgment Calls
    *Matching Shape to Problem: I made the definitive architectural call that because my core problem is a linear mathematical equation (Percent Change $\rightarrow$ Rolling Average $\rightarrow$ $S$ Score), the physical architecture must match that linear shape.

    *Avoiding Anti-patterns: I determined that artificially splitting sequentially dependent mathematical steps into separate networked services provides zero business value and introduces massive data integrity risks.
    
    *Enforcing Testability: I judged that strictly enforcing fast, isolated unit tests was the only way to mathematically guarantee the "OVERBUY" recommendation would be accurate before the business spent millions of dollars on inventory.