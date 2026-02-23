# Project Drift: Foundation 1 Overview

This document outlines the foundation work, architectural decisions, and datasets used for the project, structured into four key segments.

---

## Segment 1: The Headline

### Dataset Selection: BLS Data Set
The **Bureau of Labor Statistics (BLS)** dataset was selected for this project over other options in the pool. The primary reasons for this choice include:
* **Ease of Access:** It features a simple API for data downloads, and pseudo-code was provided to streamline the process.
* **Comprehensive Metrics:** The data focuses on key labor indicators, including **Quit Rates**, **Job Openings Levels**, and **Hires Levels**.
* **Support & Visualization:** The BLS provides a dashboard for quick visualization, and API V2 access was granted within an hour of requesting it.

### Key Learnings and Challenges
* **Data Interaction:** By working directly with the data, a clear correlation was identified between the two selected datasets.
* **Technical Hurdles:** The most difficult aspect of the process was identifying specific table names for the data, as the website structure was not straightforward.

---

## Segment 2: Characteristics and Trade-Offs

### Candidate Architecture Characteristics
The project prioritizes two specific architectural characteristics:
1.  **Interoperability:** Labor market data is insufficient in isolation. To measure a real retention gap, external BLS/JOLTS data must be connected with internal HR data. Without this connection, the system only identifies general trends rather than specific company risks.
2.  **Reliability:** This is a critical requirement. Because these signals influence major financial decisions—such as retention bonuses or hiring freezes—incorrect alerts could lead to wasted capital or the loss of valuable talent.

### Architectural Trade-Offs
There is a direct trade-off between **Performance** and **Reliability**.
* **The Conflict:** While cached data or simple rules can make dashboards update faster (high performance), reliability requires fresh JOLTS data checks and deep validation against internal records.
* **The Sacrifice:** To prioritize **Reliability**, performance (latency) must be sacrificed. This allows for longer processing times to ensure "Flight Radar" signals are 100% accurate before reaching executive stakeholders.

### The Unknown: Agility
Agility remains the hardest characteristic to assess currently. The true flexibility of the system can only be proven when the job market undergoes a sudden, unexpected change. Until then, the system is prepared for agility, but it cannot be fully verified.

---

## Segment 3: The Case Against Your Choices

### Alternative Datasets
A strong argument could be made for choosing datasets like **EIA** or **FAA**. These datasets update much faster (hourly) compared to the BLS (quarterly or monthly). Moving to these sources would force the development of streaming pipelines and the handling of concurrency, whereas the BLS dataset is primarily a batch-processing challenge.

### Architectural Weaknesses
The weakest problem architecturally is **Optimizing Compensation**. This task involves comparing internal salaries against BLS averages—a straightforward data comparison that does not require complex architectural design.

### Data Richness Defense
If challenged on the richness of the BLS dataset for a long-term project, it is important to note:
* BLS data evolves over time, requiring the model to be updated frequently.
* Matching **NAICS** (industry) and **SOC** (job) codes presents a significant technical challenge that adds depth to the project.

---

## Segment 4: AI Collaboration

### AI Usage and Helpfulness
AI was most helpful in harmonizing two project options: the "Talent Flight Radar" for retention/compensation interventions and the "Employee Flight-Risk Benchmarking" (The Retention Gap). 

### Future Improvements
For the next phase (Foundation 2), the goal is to utilize more refined prompting to ensure AI assistance provides information that is more specifically applicable to the project and the nuances of the dataset.

### Foundation 1 Summary
* **What I understand well:** Identifying industry and occupation codes.
* **Area of least confidence:** Optimizing AI prompts for more effective collaboration in Foundation 2.
