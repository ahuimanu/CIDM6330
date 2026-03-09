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



# AI Collaboration Log - Foundation 2

## Style selection dialogue: 
If you asked AI about architecture styles, what did you ask? What did it recommend? Did you follow, modify, or reject its guidance?

Based on my project, I asked AI to show me the pros and cons of all architectural styles. 

It recommended the pipeline architectural style below and I followed the guidance because it seems logical as it pertains to my project.

## Architecture Style Selection Analysis


| Architectural Style | **Pros for The Talent Sentinel** | **Cons for The Talent Sentinel** |
| :--- | :--- | :--- |
| **Layered** | Simple to understand and cheap to build, making it ideal for small teams or simple domains. | High risk of the "Architecture Sinkhole" anti-pattern where requests pass through layers without adding value. |
| **Modular Monolith** | Localizes changes to specific business capabilities, providing a clear evolution path to distributed services. | Adds unnecessary structural complexity for a project that is primarily a data transformation flow. |
| **Pipeline (Selected)** | **Best Fit.** Optimizes for sequential data transformation workflows and allows filters to be tested in isolation. | A single slow stage bottlenecks the entire system, and stage failure stalls the pipeline. |
| **Microkernel** | Ideal if the project needs to support variable "plug-ins" for different public agency data formats while keeping the core stable. | If the "Delta" logic is not properly isolated, the core system can become bloated and difficult to maintain. |


## Problem refinement: 
How did AI help (or not help) you narrow from candidates to commitment?
AI helped by discovering and identifying the secondary public sector portals such as California's State Controller (Open Payroll) or City of Austin Open Data.


## Where AI was wrong or unhelpful: 
Specific instances where AI suggestions didn't fit your context. What did you do instead?

I know that I can't access private organizational HR Database because of confidential information so I had to restrict the problem scope to what I can resolve using public data that is available online.

AI refined my intial problem statement and made it more global to include workforce retention of private companies which HR dataset that contains confidential employees information and unavailable online. Therefore, this was an unhelpful suggestion that didn't fit the context of my project and was out of scope.



# AI Collaboration Log - Foundation 3
## Process description: 
How are you working with AI? What's your workflow? When do you invoke AI assistance and when do you work independently?

  I use AI mainly as a support tool during development. My typical workflow is to ask AI to generate initial code snippets for specific parts of the project, then I run each script locally and test it independently. I only accept the code after verifying that it works as intended in my environment. For implementation and validation, I work hands-on and make the final decisions myself.

## Decision log: 
For significant decisions (architecture changes, implementation approaches, debugging strategies), document:

* What you asked the AI
* What it suggested
* What you did (accepted, modified, rejected)
* Why you made that choice


AI was especially helpful in researching whether this project required a distributed systems approach. Based on the scale of the problem, the data pipeline and workload are relatively small, so a distributed system would introduce unnecessary complexity without adding much value. After reviewing AI’s suggestions and considering the project requirements, I decided to keep the solution simpler and more practical.


## AI failures:
Specific instances where AI-generated code didn't work, was wrong, or didn't fit your context. What did you do?

There were several cases where AI-generated code did not fully fit my project context. For example, some code snippets used incorrect BLS series_id values or inserted placeholders instead of real inputs. When that happened, I did not use the output as-is. Instead, I researched the correct identifiers and replaced the incorrect values before moving forward.


## Verification practices: 
How do you verify AI-generated code works? How do you verify it's correct?

I verify AI-generated code by testing each module independently on my local machine. I check that the script runs successfully, produces the expected output, and matches the intended purpose of that part of the project. This helps me confirm both functionality and correctness before I integrate the code into the larger pipeline.

## Judgment patterns:
 Where do you find yourself consistently overriding AI suggestions? What patterns are emerging in your collaboration?

A consistent pattern in my work with AI is that I often need to override suggestions when the prompt does not include enough project-specific context. Without enough detail, AI may return generic code that does not match the actual API version, parameters, or required inputs. In this project, for example, I used version 2 of the API, but some AI-generated snippets inserted placeholder values instead of valid request parameters. This showed me that AI is useful for accelerating development, but careful review and human judgment are still necessary.
