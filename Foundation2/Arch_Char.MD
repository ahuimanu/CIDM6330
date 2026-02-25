# Architecture Characteristics - Driving and Implicit

## Driving characteristics:

### Auditability(Cross-Cutting):
    * Why is this critical? The Shortage Scout triggers high-stakes financial decisions (e.g., a $50M inventory overbuy). Because economic data is often retroactively revised by the Federal Reserve months later, the system must capture exactly what the data looked like on the day the decision was made to financially defend the recommendation.

    * How would you measure it? Success is measured by the ability to fully reconstruct a past recommendation. An engineer must be able to query a past date and retrieve the exact raw JSON payloads from FRED, the intermediate rolling averages, and the final $S$ score that generated the "OVERBUY" flag.

    * What happens if you fail? If the system triggers a massive purchase, but the predicted shortage never happens, the CFO will demand an explanation. Without point-in-time auditability, the architecture cannot prove it made a mathematically sound decision based on the data available at the time, resulting in a total loss of business trust.

### Data Integrity(Cross-Cutting): 
    * Why is this critical? The architecture ingests data with fundamentally incompatible units (Index points, Percentages, and Millions of Dollars). Maintaining data integrity during the "Unit Normalization" phase (calculating percent change) is critical because the final $S$ score logic gate requires mathematically unified inputs to function

    * How would you measure it? Success is measured by implementing automated unit tests at the transformation boundary. The system will be measured on its ability to assert that all raw values have been successfully converted into percentages (e.g., between -1.0 and 1.0) before the $S$ score calculation is allowed to execute.

    * What happens if you fail? If data integrity fails silently (e.g., the system accidentally adds $300 Million to an Index value of 100), the system will output a mathematically fraudulent "OVERBUY" recommendation, potentially costing the company millions in misallocated capital without triggering any system crash alerts.

### Testability (Structural)
    * Why is this critical? The pipeline relies on complex, sequential math. Engineers must be able to verify this logic instantly without waiting 3 months for real-world FRED data to change.
    
    *How would you measure it? Success is measured by the ability to execute automated unit tests on isolated transformation functions. An engineer must be able to inject a static, "mock" JSON payload into the pipeline and verify the exact expected $S$ score output in under 5 seconds, without making a live network call to the FRED API.

    *What happens if you fail? If the pipeline's logic is tightly coupled to the live API and cannot be tested in isolation, debugging becomes incredibly slow. Worse, untested logic updates will be pushed to production, leading directly to the silent "Data Integrity" failures (mathematically fraudulent recommendations) previously identified.

## Implicit characteristics: 

### Security 
    * The system must securely manage credentials (e.g., storing the FRED_API_KEY in secure environment variables, not hardcoded in the script). Additionally, the final output JSON must be access-restricted so competition can't leverage "OVERBUY" triggers. 

### Cost (Affordablity)
    * The pipeline only needs to execute a lightweight batch job once a month, the architecture should operate on negligible infrastructure costs (e.g. scheduled GitHub Actions) rather than paying for expensive, always-on servers.

### Deployability
    * Deployability: The underlying Python scripts and transformation logic must be easily packageable (e.g., via a Docker container or standard requirements.txt) so they can be reliably deployed to a cloud environment without complex manual setup.