# 1. Dataset Selection Justification

    Student: Nkeonyelu Igboanugo
    Course: CIDM 6330 - Software Architecture
    Date: February 8, 2026
    Branch: Foundation_1_Assignment_Nkeonyelu_Igboanugo


## Source and scope
For this project, I'll be using dataset from BLS Job Openings and Labor Turnover Survey (JOLTS)

## Access verification
I was able to request for API token for v2 access and was granted. Here is a code snippet for accessing the tables listed above tables.

```
import requests
import json
import prettytable
headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['JTS000000000000000QUR','JTS000000000000000JOL', 'JTS000000000000000HIR'],"startyear":"2011", "endyear":"2014"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)
for series in json_data['Results']['series']:
    x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes=""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
            x.add_row([seriesId,year,period,value,footnotes[0:-1]])
    output = open(seriesId + '.txt','w')
    output.write (x.get_string())
    output.close()
```

## Relational depth
To build this project, I will join the jt.data (Fact Table) and jt.series (Metadata Table) from the BLS JOLTS database.

The Relationship: These tables are linked by a common column called series_id.

* jt.data contains the raw monthly values (e.g., a "3.4" quit rate).

* jt.series acts as a decoder ring, mapping each ID to its specific industry, region, and data element.

Joining them is essential to transform abstract numbers into meaningful insights, like comparing your company’s turnover to the "Professional and Business Services" sector.


## Temporal characteristics
For the JOLTS dataset, the specifics are as follows:

* Update Frequency: Monthly. Data is typically released about 35 days after the reference month ends (e.g., October data is released in early December).

* Historical Depth: Continuous records date back to December 2000, providing over 25 years of labor market context.

* Time Granularity: The data is strictly monthly. While hourly or daily snapshots do not exist, the BLS provides annual totals and averages derived from these monthly series.

## Why this dataset
The "Talent Sentinel" is compelling because it transforms dry BLS data into a strategic command center. By calculating the Retention Delta, it distinguishes between internal culture failures and macro-market trends.

Business Impact: It prevents "panic spending" by replacing broad raises with surgical, data-driven interventions. If you outperform the market, you pivot to aggressive recruitment; if you lag, you trigger targeted retention. This optimization reduces turnover costs and protects margins, turning HR into a profit-protecting engine rather than a cost center.


# 2. Initial Problem Space
## Domain observations
In the BLS JOLTS data, I noticed a lagged correlation between Job Openings and Quits; as openings spike, quits follow with a distinct delay. A significant anomaly appears in 2020-2021, where the "Great Resignation" created a historic decoupling from long-term averages.

Data Gaps: Sector-level granularity is inconsistent, with broader categories (Total Nonfarm) offering deeper history than specific sub-sectors. Additionally, the 35-day reporting lag creates a "blind spot" for real-time volatility.

## Candidate problems
* Optimizing Compensation: Determine if wage increases are necessary to compete with rising sector-specific hire rates.

* Resource Allocation: Decide whether to invest in "Culture Fixes" or "Recruitment Marketing" based on the industry Retention Delta.

* Headcount Planning: Predict future hiring difficulty by monitoring the ratio of job openings to available hires.

* Budget Forecasting: Anticipate retention bonus needs before "Quit Rate" spikes occur based on leading market heat signals.

## Questions you can't yet answer
To choose among these problems, you need to evaluate three critical factors:

* Feasibility: Is your internal HR data (granularity by department/role) clean enough to map to BLS industry sectors?

* Value: Which problem aligns with your current corporate priority? (e.g., Is your board more worried about hiring speed or retention costs?)

* Scope: Are you targeting a national strategy or a regional one? BLS JOLTS offers national and state-level data, but not specific metropolitan area detail for all industries.


# 3. Architecture Characteristics Discovery

## Candidate characteristics
For a system integrating BLS labor data, these architectural characteristics are critical:

* Interoperability: Connects external BLS APIs seamlessly with internal HRIS databases.

* Scalability: Manages the increasing volume of historical JOLTS records and internal data.

* Reliability: Ensures "Flight Radar" signals are accurate for high-stakes financial decisions.

* Agility: Allows the system to pivot quickly as labor market dynamics evolve.

* Testability: Validates that "Retention Delta" formulas accurately reflect reality.

* Deployability: Facilitates seamless monthly updates synced with BLS data releases.

* Performance: Provides low-latency analysis for real-time executive dashboards.

## Tensions you anticipate
In this system, a primary conflict arises between Performance and Interoperability. Fetching and joining massive external BLS datasets with internal HRIS records in real-time can create significant latency.

Another trade-off is Agility versus Reliability. Rapidly updating "Flight Radar" logic to meet evolving market trends (Agility) can inadvertently introduce bugs into the "Retention Delta" formulas, compromising the data's integrity for financial interventions (Reliability). Balancing these requires a robust automated testing suite, which adds complexity and may further impact deployment speed.

## What you don't know yet
If the goal is an Executive Dashboard, high Availability is paramount for on-demand board meetings. However, if the system is a Batch Processor generating monthly reports, occasional downtime is acceptable.

Similarly, Elasticity depends on scale: a tool for a small firm requires minimal resource scaling, whereas a global enterprise analyzing thousands of departments across multiple BLS sectors would require a system that dynamically scales to handle heavy computation.
