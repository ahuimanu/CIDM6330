# AI Collaboration Log - Foundation 1
    Student: Nkeonyelu Igboanugo
    Course: CIDM 6330 - Software Architecture
    Foundation_1: Dataset Selection 
    Date Range: February 8, 2026

## Session 1: Harmonizing 2 Business Projects Ideas


### What you asked 
* I asked AI to harmonize two business sample problems that I came up with about Talent and HR using BLS data. 
* I then requested AI to come up with 4 problems better than my 2 sample problems, again constrained to BLS datasets/series IDs.

 

### What you got 
* AI came up with a framework to build a real-time dashboard that integrates internal HR turnover data with BLS macroeconomic signals to determine if a company’s "Flight Risk" is caused by internal culture or market heat, and then trigger automated financial or recruitment interventions.
* It also returned candidate directions like compensation optimization, resource allocation (culture fixes vs recruiting), headcount planning, and bonus budgeting, which align with your stated candidate problems. 


 
### What you used, modified, or rejected 
* Used: I adopted JOLTS as the core dataset and explicitly used the same three series IDs for access verification (QUR, JOL, HIR) and included a working API call snippet to prove feasibility. 

* Used: I incorporated the architecture rationale that I will join jt.data (fact) with jt.series (metadata) to turn abstract series IDs into interpretable sector/region metrics. 

* Modified: The output “ideas” were tightened into a clearer central value proposition: my write-up positions the tool as a strategic command center that reduces “panic spending” by separating macro-market trends from internal issues (“Retention Delta”). 

* Rejected: I noted limitations (sector granularity inconsistencies; ~35-day lag) and this likely pushes me away from any claim of “real-time” labor-market monitoring. 

### Your judgment calls 
* I constrained scope to what I can prove: I didn’t just accept a broad concept but added an API token confirmation + working extraction snippet.

* I corrected the “real-time” temptation: By calling out the 35-day reporting lag and “blind spot,” you set realistic expectations and avoided overselling timeliness. 

* I kept decision questions open instead of inventing internal data: I flagged feasibility/value/scope questions about mapping internal HR data to BLS sectors, which is a conservative way to avoid assuming data you don’t actually have.



## Session 2: Data and Architectural Feasibility Study
### What you asked
I used AI primarily to help clarify and structure my thinking around dataset selection and problem framing. Specifically, I asked questions about:
* Which BLS datasets would be architecturally interesting for a software architecture project
* How JOLTS data could support a real business problem beyond simple reporting
* How to articulate relational depth, temporal characteristics, and architectural trade-offs in a clear, academic way
* How to frame an initial problem space that was realistic, defensible, and grounded in the data


### What you got
The AI provided:
* Suggestions for framing JOLTS as a leading-indicator system rather than a descriptive dashboard
* Language to explain why joining jt.data and jt.series adds relational and analytical value
* Examples of business problems (e.g., retention vs. recruitment decisions) that could plausibly be supported by JOLTS
* Help identifying architectural characteristics (scalability, interoperability, reliability) and likely trade-offs



### What you used, modified, or rejected
* Used: High-level framing ideas, such as positioning the project as a decision-support or “early warning” system and emphasizing temporal lag relationships (e.g., job openings leading quits).
* Modified: Almost all language. I rewrote explanations in my own words, adjusted the tone to be more conservative, and aligned the scope with what JOLTS can actually support (national and state-level, monthly data).
* Rejected: Any suggestions that implied real-time analytics, metro-level precision, or causal certainty. I also avoided overstating business impact or claiming predictive accuracy beyond what the data reasonably allows.



### Your judgment calls
I made several judgment calls where I overrode or extended AI suggestions:
* I limited claims about insight and prediction to what monthly, lagged BLS data can realistically support.
* I explicitly called out data gaps and constraints (reporting lag, sector granularity), even when AI framing leaned more optimistic.
* I chose to emphasize architectural trade-offs (performance vs. interoperability, agility vs. reliability) rather than focusing only on technical features, because that better fits a software architecture lens.
* I decided to frame the system as potentially batch-oriented rather than always-on, reflecting uncertainty about actual usage and availability requirements.




