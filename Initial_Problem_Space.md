# Initial Problem Space

**Student:** Zane Hill  
**Course:** CIDM 6330 - Software Architecture  
**Date:** January 31, 2026  
**Branch:** Foundation-1-Zane-Hill

---

## Domain Observations

### What I Noticed When Exploring the Data

#### 1. **Revision Patterns Are Significant**

When examining the GDP series metadata, I noticed the data includes `realtime_start` and `realtime_end` fields for every observation. This reveals that economic data undergoes substantial revisions:

```
GDP for Q1 2024 might show:
  - April 30, 2024 (advance):   $27,620.5B
  - May 30, 2024 (second):      $27,632.1B  
  - June 27, 2024 (third):      $27,645.3B
  - July 2025 (annual revision): $27,673.2B
```

**Observation:** Initial releases can differ from final values by hundreds of billions of dollars. This has real implications:
- Financial models built on preliminary data may be wrong
- Policy decisions made with incomplete information
- "What did we know then?" becomes a critical architectural question

**Gap Identified:** Standard time series systems don't typically model this bi-temporal nature (observation date vs. knowledge date).

#### 2. **Catastrophic Events Create Data Anomalies**

Looking at the unemployment rate (UNRATE) data from 2020:

```
2020-02-01: 3.5%  (Pre-pandemic normal)
2020-03-01: 4.4%  (Shutdowns begin)
2020-04-01: 14.8% (Peak crisis - 4x increase in one month)
2020-05-01: 13.2%
2020-06-01: 11.0%
```

**Observation:** A single month saw unemployment quadruple - an unprecedented shock. This creates challenges:
- Historical patterns become unreliable for forecasting
- Simple moving averages are distorted for years
- "Normal" data vs. "crisis" data need different treatment

**Pattern:** Major economic shocks (2008 financial crisis, 2020 pandemic, etc.) fundamentally break statistical assumptions. Systems need to detect and handle regime changes.

#### 3. **Update Frequencies Are Domain-Constrained**

Different series update on radically different schedules:

| Series | Frequency | Why? |
|--------|-----------|------|
| Federal Funds Rate | Daily | Markets trade daily |
| Unemployment | Monthly | Survey takes time to compile |
| GDP | Quarterly | Complex accounting requires aggregation |
| Annual Deficit | Yearly | Fiscal year accounting |

**Observation:** You can't just "refresh the dashboard" - each indicator has its own natural cadence determined by how it's measured. A system that checks GDP daily is wasting resources; one that checks Fed Funds monthly is dangerously stale.

**Architectural Implication:** Need intelligent scheduling based on release calendars, not naive polling.

#### 4. **Series Relationships Are Complex and Implicit**

When searching for "inflation," I got 5+ different series:
- CPI (Consumer Price Index)
- PCE (Personal Consumption Expenditures) 
- CPI Core (excluding food/energy)
- 10-Year Breakeven Rate (market-implied)
- Various inflation-indexed bond yields

**Observation:** There's no single "inflation" - different measures for different purposes:
- Fed targets PCE, not CPI
- Headlines report CPI
- Markets price inflation expectations via TIPS spreads
- Core vs. headline matters for policy

**Gap:** The API doesn't explicitly encode these semantic relationships. A user asking "what's inflation?" requires domain knowledge to select the right series.

#### 5. **Regional Granularity Varies Wildly**

Found data at multiple geographic levels:
- National (all series)
- State-level (unemployment, GDP by state)
- MSA/Metro-level (some employment data)
- County-level (limited, mostly census-derived)

**Observation:** Can't do uniform geographic analysis - available granularity depends on the indicator. Unemployment is richly detailed geographically; monetary policy indicators are national only.

**Pattern:** "Show me all indicators for Austin, TX" is impossible - you'd get employment data but not local Fed Funds rate (which doesn't exist).

#### 6. **Seasonal Adjustment Is Inconsistent**

Many series come in pairs:
- UNRATE (seasonally adjusted)
- UNRATENSA (not seasonally adjusted)

**Observation:** Seasonal effects are real (construction employment drops in winter), but adjustment methods vary. Some series only exist in one form. Mixing adjusted and unadjusted data creates meaningless comparisons.

**Anomaly:** The API returns both in search results but doesn't clearly flag which is which without reading documentation.

#### 7. **Missing Data Is Common and Meaningful**

Saw observations with `value: null` (represented as "." in raw API):
- Series that start mid-history
- Discontinued series that end
- Data embargoes or confidentiality gaps

**Observation:** Missing data isn't just "no measurement" - it often signals:
- Series definition changed (BLS revised methodology)
- Confidentiality (too few respondents to publish without disclosure risk)
- Political sensitivity (some international data)

**Gap:** Need to distinguish "not yet released," "permanently discontinued," "temporarily withheld," and "measurement not applicable."

#### 8. **Popularity Metrics Suggest Usage Patterns**

Series metadata includes `popularity` scores:
- GDP: 95
- UNRATE: 88
- Obscure regional series: <10

**Observation:** A small number of series get vast majority of attention. This suggests:
- Caching strategy should focus on hot series
- UI should surface popular series first
- Most of the 840,000 series are rarely accessed

**Pattern:** Power law distribution - 1% of series probably account for 80%+ of requests.

---

## Candidate Problems

### Concrete Business Problems This Dataset Could Address

#### Problem 1: **Real-Time Economic Indicator Dashboard for Financial Services**

**Specific Problem:** Investment advisors need to monitor 15-20 key economic indicators (Fed Funds, unemployment, CPI, GDP, etc.) and be alerted within minutes when new data releases, as these releases move markets.

**Use Case:**
- 8:30 AM ET: BLS releases employment report
- System immediately fetches new data via FRED API
- Calculates change vs. forecast and historical patterns
- Pushes alert: "Unemployment dropped to 3.7% (expected 3.9%) - surprise!"
- Portfolio managers adjust positions before market fully reacts

**Data Elements Needed:**
- Real-time observation data for ~20 series
- Historical baselines (12-month average, YoY change)
- Release schedules (to know when to poll)
- Analyst forecast consensus (not in FRED - would need external source)

**Why FRED Works:** Daily updates for key series, reliable API, covers all major indicators used by finance professionals.

**Success Metric:** Deliver alerts within 60 seconds of data release appearing in FRED.

---

#### Problem 2: **Economic Revision Impact Analyzer for Policy Research**

**Specific Problem:** Economic policy researchers need to understand how often preliminary data is wrong and by how much, to assess whether decisions made on initial data were based on accurate information.

**Use Case:**
- Researcher studying 2008-2009 recession
- Question: "Did policymakers underestimate the crisis because initial GDP numbers weren't as bad as final revisions showed?"
- System retrieves all vintage dates for GDP Q4 2008 through Q2 2009
- Compares advance, second, third estimates vs. final revised numbers
- Visualizes how understanding of crisis evolved over time
- Quantifies revision magnitude and timing

**Data Elements Needed:**
- ALFRED vintage dates for major series (GDP, employment, income)
- Multiple revision cycles per observation
- Ability to query "what was GDP on 2009-03-01?" (as it existed then)
- Statistical measures of revision patterns

**Why FRED Works:** ALFRED is unique in maintaining complete revision history - most data sources only keep current values.

**Success Metric:** Generate report showing revision impact for any economic episode (recessions, recoveries, policy changes).

---

#### Problem 3: **Regional Economic Health Monitoring for Municipal Governments**

**Specific Problem:** City economic development offices in mid-sized cities (Austin, Amarillo, Lubbock) need to track their local economy vs. state and national trends to make informed decisions about incentives, workforce programs, and budget planning.

**Use Case:**
- Austin economic development office wants monthly dashboard
- Compare Austin MSA unemployment to Texas state and US national
- Track local employment trends by sector
- Monitor housing market indicators (permits, prices)
- Identify if Austin is outperforming or underperforming
- Flag when local trends diverge from state/national

**Data Elements Needed:**
- MSA-level employment and unemployment data
- State-level comparisons
- National benchmarks
- Time series covering 5-10 years for trend analysis
- Multiple sectors (total, manufacturing, services, government, construction)

**Why FRED Works:** Rich state and MSA-level employment data from BLS, consistently formatted for comparison.

**Success Metric:** Monthly report showing Austin's position vs. benchmarks with statistical tests for significant divergence.

---

#### Problem 4: **Monetary Policy Educational Simulator for Economics Students**

**Specific Problem:** Undergraduate economics students struggle to understand how Federal Reserve decisions (interest rates) ripple through the economy, affecting unemployment, inflation, and growth - they need an interactive tool showing historical cause-and-effect.

**Use Case:**
- Student selects historical period (e.g., "2007-2009 Financial Crisis")
- System displays timeline of Fed Funds rate changes
- Overlays unemployment, GDP growth, inflation on same chart
- Student can see lag effects: "Fed cuts rates in Nov 2008, but unemployment keeps rising for 6 more months"
- Comparison mode: "2008 crisis vs. 2020 pandemic" - different Fed responses, different outcomes
- Quiz mode: "It's March 2020, unemployment is spiking - what should Fed do?"

**Data Elements Needed:**
- Federal Funds rate (daily)
- Unemployment rate (monthly)
- GDP (quarterly)
- Inflation (monthly)
- Must cover multiple business cycles (50+ years)
- Annotations for major Fed policy decisions

**Why FRED Works:** Long historical coverage (1950s onward), all key macro indicators in one place, free access for educational use.

**Success Metric:** Students can correctly predict directional impacts of policy changes and explain lag effects.

---

#### Problem 5: **Automated Economic Newsletter Generator for Small Businesses**

**Specific Problem:** Small business owners (restaurants, retail, services) don't have time to follow economic data but need to understand business conditions - "Is the economy growing? Are consumers spending? Should I hire?"

**Use Case:**
- Weekly automated email newsletter
- "Economic Update for Texas Business Owners"
- Pulls latest data: unemployment, consumer spending, retail sales, wages
- Translates into plain English: "Unemployment fell to 3.8% - workers are harder to find, you may need to raise wages"
- Flags major changes: "⚠️ Consumer spending dropped 2% - customers may be tightening budgets"
- Regional focus: Texas-specific data + national context
- No jargon, actionable insights

**Data Elements Needed:**
- Consumer spending indicators (retail sales, PCE)
- Labor market (unemployment, wage growth)
- State-level data for regional context
- Month-over-month and year-over-year changes
- Historical context ("highest since 2019")

**Why FRED Works:** Comprehensive coverage of business-relevant indicators, reliable updates, state-level detail.

**Success Metric:** Business owner can explain local economic conditions in 2-minute read.

---

## Questions I Can't Yet Answer

### Feasibility Questions

#### 1. **What Are FRED API Rate Limits?**

**What I Know:** Free API access with key-based authentication.

**What I Don't Know:**
- Requests per second/minute/hour/day limits?
- Are there different tiers (academic vs. commercial)?
- How does FRED handle burst traffic (e.g., during major data releases)?
- Are there bulk download options for historical data?

**Why It Matters:** 
- Problem 1 (real-time dashboard) needs frequent polling
- Problem 2 (revision analyzer) might need thousands of vintage date queries
- Need to know if architectural approach must include caching/throttling

**How to Find Out:** 
- Review FRED API Terms of Service
- Test with burst requests and monitor for rate limit errors
- Contact FRED support for official policy

---

#### 2. **How Reliable Is FRED Uptime During Critical Release Windows?**

**What I Know:** API was accessible during my testing.

**What I Don't Know:**
- Does FRED ever go down during high-traffic moments (e.g., 8:30 AM employment releases)?
- What's typical latency from official release to FRED API availability?
- Are there redundancy options or backup data sources?

**Why It Matters:**
- Problem 1 (financial dashboard) is time-sensitive - minutes matter
- Need SLA understanding for production deployment
- May need fallback architecture

**How to Find Out:**
- Study FRED uptime history
- Monitor API during actual release events
- Ask FRED community about outage experiences

---

#### 3. **Can I Efficiently Query Related Series Without Knowing IDs in Advance?**

**What I Know:** Must specify exact series_id (e.g., "GDP", "UNRATE").

**What I Don't Know:**
- Can I say "give me all state unemployment rates" without listing 50 series IDs?
- How do I discover related series programmatically?
- Is there a "series family" or "collection" concept?

**Why It Matters:**
- Problem 3 (regional monitoring) needs MSA-level data - how many series IDs?
- Problem 5 (newsletter) needs dynamic series selection based on relevance
- Manual ID lists are brittle and incomplete

**How to Find Out:**
- Explore category and tag endpoints more deeply
- Test bulk retrieval patterns
- Review FRED API v2 documentation (mentioned for bulk operations)

---

#### 4. **What's the Quality of Regional/Local Data?**

**What I Know:** National data is comprehensive and timely.

**What I Don't Know:**
- Are MSA-level indicators as current as national (same-day updates)?
- Do smaller metros have data gaps or longer lags?
- Which indicators are NOT available below state level?

**Why It Matters:**
- Problem 3 (regional monitoring) depends on local data quality
- Can't promise monthly updates if MSA data is quarterly or spotty
- May need to combine FRED with other regional sources

**How to Find Out:**
- Query specific MSA series (Austin, Lubbock, Amarillo) and check dates
- Compare update frequencies national vs. regional
- Review BLS source documentation on geographic coverage

---

### Value Questions

#### 5. **Is Real-Time Economic Data Valuable Enough to Pay For?**

**What I Know:** FRED data is free.

**What I Don't Know:**
- Would financial firms pay for faster access (milliseconds matter in trading)?
- Do Bloomberg/Reuters offer lower-latency economic data feeds?
- Is there a market for "FRED plus" with better tooling?

**Why It Matters:**
- Problem 1 (financial dashboard) might need paid data sources if FRED is too slow
- Business model question: is this a free tool or paid service?
- May affect architecture (optimize for cost vs. speed)

**How to Find Out:**
- Research financial data vendor offerings
- Interview potential users (financial advisors, traders)
- Understand competitive landscape

---

#### 6. **Do Users Actually Want Historical Revision Analysis?**

**What I Know:** ALFRED exists and maintains revision data.

**What I Don't Know:**
- How many researchers/analysts actually use revision data?
- Is this a niche academic interest or practical business need?
- Would users pay for revision analytics tools?

**Why It Matters:**
- Problem 2 (revision analyzer) is technically feasible but is there demand?
- If user base is tiny, may not justify development effort
- Need to validate problem exists before building solution

**How to Find Out:**
- Survey economists, policy analysts, financial researchers
- Check ALFRED usage statistics (if available)
- Review academic literature citing ALFRED

---

#### 7. **Can Non-Economists Interpret Economic Data Correctly?**

**What I Know:** Economic indicators are complex (CPI vs. PCE, seasonal adjustment, etc.).

**What I Don't Know:**
- Will small business owners (Problem 5) misinterpret simplified data?
- Do I need disclaimers about data limitations?
- Is there liability risk in providing automated economic advice?

**Why It Matters:**
- Problem 5 (newsletter) aims to democratize economic data
- Risk of oversimplification leading to bad decisions
- May need expert review or conservative framing

**How to Find Out:**
- User testing with non-economist business owners
- Consult with economists on appropriate simplification
- Legal review of disclaimers and limitations

---

### Scope Questions

#### 8. **Should I Integrate Multiple Data Sources or Stay FRED-Only?**

**What I Know:** FRED has 840,000+ series but isn't exhaustive.

**What I Don't Know:**
- What key data is missing from FRED? (Company earnings, commodity prices, international detail?)
- Would problems be better solved with FRED + World Bank + Census + BEA APIs?
- Does integration complexity outweigh benefits?

**Why It Matters:**
- Problem 3 (regional monitoring) might benefit from Census demographic data
- Problem 1 (financial dashboard) might need market data (S&P 500, bond yields)
- Architecture complexity scales with number of data sources

**How to Find Out:**
- Map candidate problems to required data elements
- Identify gaps not covered by FRED
- Assess integration effort for additional sources

---

#### 9. **What's the Right Scope for a Semester Project?**

**What I Know:** Have 3-4 months for development.

**What I Don't Know:**
- Is a full production system achievable or should I focus on proof-of-concept?
- Should I build one problem deeply or explore multiple lightly?
- What's the balance between architectural exploration vs. feature completeness?

**Why It Matters:**
- Problems 1-5 vary dramatically in complexity
- Need to set realistic scope to deliver quality work
- Academic project goals differ from commercial product goals

**How to Find Out:**
- Review course expectations and grading criteria
- Discuss with professor what level of completion is expected
- Look at past student projects for scope benchmarks

---

#### 10. **Which Architectural Patterns Should I Prioritize Demonstrating?**

**What I Know:** Course is about software architecture, not just building an app.

**What I Don't Know:**
- Should I focus on data architecture (storage, caching, querying)?
- Or service architecture (microservices, APIs, event-driven)?
- Or deployment architecture (containers, cloud, scaling)?
- How many patterns can I meaningfully implement in one semester?

**Why It Matters:**
- Different candidate problems showcase different architectural concerns
- Problem 1: caching, real-time updates, event-driven
- Problem 2: historical querying, data versioning, batch processing
- Problem 3: multi-tenancy, reporting, aggregation
- Need to choose problems that align with learning objectives

**How to Find Out:**
- Review course syllabus for architectural topics covered
- Identify which patterns are most valuable to learn
- Select candidate problem that best demonstrates target patterns

---

## Next Steps

To move from this problem space exploration to Foundation 2 (Problem Definition), I need to:

1. **Test API Limits** - Run performance tests to understand rate limits and latency
2. **Validate User Interest** - Interview potential users for Problems 1, 3, or 5
3. **Scope Reality Check** - Assess what's achievable in semester timeframe
4. **Choose Architectural Focus** - Align problem selection with course learning objectives
5. **Data Quality Audit** - Deep dive into regional/local data completeness

These investigations will inform selection of one specific problem to define and solve in Foundation 2.

---

**Repository:** `Foundation-1-Zane-Hill` branch  
**Related Files:**
- `FRED_Data_Retrieval.py` - API implementation
- `Dataset_Selection_Justification.md` - Dataset documentation
- `fred_data/` - Sample retrieved data
