# Problem Definition

    Student: Nkeonyelu Igboanugo
    Course: CIDM 6330 - Software Architecture
    Date: February 22, 2026
    Branch: Foundation_2_Assignment_Nkeonyelu_Igboanugo

## Problem Statement
The Talent Sentinel (Public Edition) addresses the critical "retention blind spot" in public sector management, specifically for state and local government agencies that struggle to compete with private sector "market heat". Public administrators often lack the analytical tools to determine if high turnover in a specific department is a localized management issue or a reflection of broader economic trends, such as a spike in private-sector "Professional Services" hiring. By integrating publicly available state workforce datasets with BLS JOLTS macroeconomic signals, this system provides a real-time command center for policy-makers to justify budget pivots, retention bonuses, or management audits based on data-driven "Flight Risk" signals.

## Why this problem
I selected this problem because it utilizes the Relational Depth and Temporal Characteristics of the BLS JOLTS data without requiring confidential corporate access. During discovery, I learned that while private data is locked away, many public agencies provide the necessary granular "voluntary termination" records required to calculate a Retention Delta. This specific problem allows for a high-impact demonstration of Interoperability (linking two different public APIs) and Reliability, which are the primary architectural characteristics identified for this project.

## Scope boundaries

* In-Scope:

    * Automated ingestion of BLS JOLTS data via the Public API v2 (Quits, Openings, and Hires rates).

    * Ingestion of at least one publicly available state or city workforce dataset (e.g., California State Controller's Office or City of Austin Open Data) that includes voluntary termination reasons.

    * Calculation of the Market Heat Index and the Risk-Adjusted Delta between the public agency and the broader industry.

    * A web-based Executive Dashboard featuring the "Radar" view and threshold-based alerts.  

* Out-of-Scope:

    * Integration with private, non-public HRIS systems (e.g., Workday or SAP).

    * Analysis of involuntary terminations, retirements, or layoffs.

    * Real-time predictive modeling (limited by the 35-day BLS reporting lag).


## Success criteria
* Attribution Accuracy: The system successfully classifies 100% of the public agency's voluntary departures into the four strategic quadrants: The Gold Standard, Market Squeeze, Internal Crisis, or Safe Zone.

* Decision Support: The dashboard identifies at least one instance where an agency's "Flight Risk" was driven by external "Market Heat" rather than internal failure, providing a data-backed justification for a retention intervention.

* Data Latency Management: The system successfully bridges the 35-day BLS lag by providing a rolling 12-month historical benchmark that aligns with the most recent public agency data release.

* Component Modularity: The architecture demonstrates high Testability and Modularity, allowing a user to swap one public agency dataset for another without modifying the core "Sentinel" logic.


# Data Pipeline Definition

## Data sources
* BLS Public API (v2): This provides the "Macro Benchmark" through the Job Openings and Labor Turnover Survey (JOLTS). Specific endpoints will pull:

    * Quits Rate: Series JTS000000000000000QUR (Total Nonfarm) and sector-specific codes (e.g., JTS900000000000000QUR for Government).

    * Job Openings and Hires Rates: To calculate the competitive strength and "Alternative Opportunity" signals.

* Public Sector Open Data Portals: These provide the "Subject Data" from portals such as California's State Controller (Open Payroll) or City of Austin Open Data.

    * Tables used: Termination/Separation records and monthly Headcount totals.

* BLS Metadata Tables: The jt.series and jt.industry tables act as a "decoder ring" to map abstract IDs to human-readable industry sectors.

## Data relationships

* Sector Correspondence: The primary link is a correlation between the public agency's "Department" or "Job Family" and the corresponding BLS Industry Sector (e.g., matching a City IT department to the Professional and Business Services sector).

* Relational Join: Within the processing engine, the jt.data fact table is joined with the jt.series metadata table using the series_id.

* Temporal Alignment: Both datasets are joined on the Year and Period (Month) keys to ensure comparisons account for the 35-day BLS reporting lag.

## Transformation requirements
* Filtering: Internal public agency records must be filtered to isolate Voluntary Terminations (Quits) only, excluding retirements or layoffs to match the BLS definition.

* Aggregation: Monthly employee-level records from the Open Data portal are aggregated into a single Agency Quit Rate percentage.

* Enrichment (Calculations): The core engine performs two primary calculations:
    * Market Heat Index: $\text{Openings} \div \text{Hires}$.

    * Relative Turnover Pressure (RTP): $(\text{Agency Quit Rate} - \text{Industry Quit Rate}) \times \text{Market Heat Index}$.

## Output shape
The pipeline outputs a structured JSON payload designed for a Real-Time Strategic Dashboard:

* The Radar View: A 12-month rolling trend comparison of the agency's performance versus the industry benchmark.

* Quadrant Assignment: Each department is assigned a status: Gold Standard, Market Squeeze, Internal Crisis, or Safe Zone.

* Trigger Alerts: High-priority notifications for Finance and HR when the RTP crosses a pre-defined risk threshold, signaling a need for budget or management intervention.

# Architecture Characteristics - Driving and Implicit

## Driving characteristics
1. Interoperability

    * Why critical: The system's core value is its ability to connect disparate external APIs (BLS JOLTS) with various public agency data formats (CSV/Socrata). Without seamless communication between these data "quanta," the Risk-Adjusted Delta cannot be calculated.

    * Measurement: Success is measured by the ability to ingest and normalize data from at least two different public sources (e.g., BLS and a State Controller's CSV) into a single unified schema without manual intervention.


    * Failure impact: If interoperability fails, the system becomes a manual data-entry tool, re-introducing the high cost and human error that the "Talent Flight Radar" is meant to eliminate.


2. Modularity


    * Why critical: This is a domain-partitioned system where "Agency Adapters" must be independently developable from the "Macro Benchmark" logic. High functional cohesion ensures that changes to the BLS API contract don't break the logic for specific city datasets.

    * Measurement: Achieved if a new public agency dataset (e.g., changing from the City of Austin to the City of New York) can be integrated by adding a new "filter" or "plugin" without modifying the core calculation engine.


    * Failure impact: Failure leads to a "Big Ball of Mud" monolith where every data update creates cascading dependencies, making the system fragile and impossible to maintain as more agencies are added.


3. Reliability

    * Why critical: Executives and Finance departments use these signals to justify significant financial interventions (e.g., retention bonuses). The system must handle the "Fallacies of Distributed Computing," specifically that the network is not reliable and latency is not zero.

    * Measurement: Measured by the system's "Fault Tolerance" rating—specifically its ability to handle a failed BLS API request without crashing the entire dashboard, perhaps by serving the last cached "Radar" view.

    * Failure impact: If the system is unreliable, it provides false "Internal Crisis" signals, leading to "panic spending" or incorrect management audits, which destroys executive trust.

## Implicit characteristics

* Security: As the system uses public-facing datasets, basic transport security (HTTPS/TLS) is assumed but not a differentiating factor for the architecture's core shape.


* Availability: While the dashboard needs to be accessible, it is not a "mission-critical" real-time system; because it relies on monthly BLS data, an hour of downtime for maintenance is acceptable and does not drive the design.

## Characteristic trade-offs

* Reliability vs. Agility: To ensure high reliability and accuracy of the "Retention Delta," we must implement rigorous automated testing between layer boundaries. This sacrifice in Agility means new data features will take longer to deploy, but it prevents the "Architecture Sinkhole" of pushing unverified data to executives.


* Modularity vs. Performance: By using a domain-partitioned approach (like a Modular Monolith or Pipeline), we accept a slight performance hit due to data transformations between components. We are willing to sacrifice sub-second latency for the ability to localise changes and scale the system to more public agencies over time.


# Architecture Style Selection

* Selected style: Pipeline Architecture
The Pipeline Architecture (also known as the pipes-and-filters pattern) is the most effective choice for this project. It organizes the system into a series of sequential processing stages (filters) connected by unidirectional channels (pipes).

* Why this style
This style directly supports your driving characteristics through its inherent structural properties:

    * Sequential Data Transformation: The project is a classic ETL (Extract, Transform, Load) workflow, which is the primary "best fit" for the Pipeline style.


    * Modularity & Interoperability: Each filter (e.g., "BLS Ingester" or "Delta Calculator") has exactly one job, making the system easy to understand and modify.


    * High Testability: Because filters are decoupled, you can test the "Retention Delta" logic in isolation without needing to mock an entire UI or database layer.


    * Filter Types: Your system perfectly maps to the four filter types: Producers (BLS/Open Data APIs), Transformers (RTP Calculator), Testers (Threshold Validators), and Consumers (Dashboard/Alerts).

* Alternatives considered

    * Layered Architecture: This was rejected because it often leads to the Architecture Sinkhole Anti-Pattern. Since the core of your project is data movement rather than complex UI interactions, requests would likely pass through layers doing nothing but calling the next layer down. It also offers weak agility when adding new data fields.

    * Modular Monolith: While this offers good domain alignment, it was deemed unnecessary for a system that is primarily a processing flow rather than a collection of interactive business capabilities (like Payments or Inventory). A modular monolith adds complexity in managing in-process module communication that a simple pipeline avoids.


* Style-specific trade-offs

    * Low Elasticity: Because the pipeline is sequential, a slow "Producer" (like a lagging BLS API) will bottleneck the entire system; you cannot easily speed up the calculation stage if the ingestion stage is stalled.


    * Fault Tolerance: A failure in a single filter (e.g., a schema change in the public agency data) will stall the entire pipeline, preventing the final "Radar" view from being generated.


    * Unidirectional Flow: This style is poor for interactive or bidirectional needs; if the dashboard needs to "talk back" to the ingestion layer frequently, the pipeline will become difficult to manage.


* Quantum analysis
This design has one architecture quantum.


    * Reasoning: Although the pipeline consists of multiple filters, they are part of a single deployment unit that shares the same operational characteristics and is scaled together.

    * Implication: Characteristics like reliability and performance apply uniformly across the entire pipeline; if the processing engine crashes, the entire "Talent Flight Radar" is unavailable.



# Component Identification

## Component inventory

* Market Ingester (Producer): Responsible for the starting point of the pipeline by fetching macroeconomic time-series data from the BLS Public API v2. It processes raw BLS Series IDs, specifically the Quits, Openings, and Hires rates.


* Agency Ingester (Producer): Acts as a parallel starting point that extracts subject-specific data from Public Open Data portals. It processes state or city workforce records, focusing on voluntary termination counts and headcount totals.


* RTP Calculator (Transformer): Responsible for converting and enriching the raw data by normalizing agency records and calculating the Market Heat Index and Relative Turnover Pressure (RTP). It processes the relationship between internal agency rates and the industry-specific peer benchmarks.


* Alert Validator (Tester): Acts as a validation gate to accept or reject signals based on predefined strategic thresholds. It processes risk scores to determine if a specific data point warrants a financial or recruitment intervention.


* Radar Dashboard (Consumer): Serves as the termination point of the pipeline where processed insights are stored or displayed for executive use. It processes the final data into a 12-month "Radar" view categorized into the four strategic quadrants.

## Partitioning approach
I am using Technical Partitioning (organized by what code does) within a Pipeline context.


* Sequential Logic: The "Talent Sentinel" is fundamentally a sequential transformation workflow rather than a collection of independent business capabilities like "Orders" or "Payments".


* Specialized Skillsets: Technical partitioning is appropriate here because the expertise required for external API ingestion is distinct from the statistical modeling required for the RTP calculation.


* Simplicity: For this data-heavy project, technical partitioning avoids the complexity of trying to force a domain structure onto what is essentially a data processing "pipe".

## Boundaries

* Component Boundaries: The boundaries exist at the Pipes between filters, which are unidirectional channels that ensure one-way data flow.

* Cohesion Type: Each component has High Functional Cohesion, meaning all elements within a filter work together toward a unified processing purpose.

* Avoiding the Entity Trap: By identifying components based on Workflow (Ingest → Calculate → Test → Display) rather than data entities like "Employee" or "Series ID," the system avoids poor cohesion and high coupling.