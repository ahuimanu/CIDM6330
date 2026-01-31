# Architecture Characteristics Discovery

**Student:** Zane Hill  
**Course:** CIDM 6330 - Software Architecture  
**Date:** January 31, 2026  
**Branch:** Foundation-1-Zane-Hill

**Reference:** *Fundamentals of Software Architecture* (Richards & Ford, 2nd ed.), Chapters 4-5

---

## Introduction

This document explores architecture characteristics (the "-ilities") that appear relevant for systems built on Federal Reserve Economic Data (FRED). Following FSA Chapter 4's guidance, I'm identifying characteristics that might drive architectural decisions, recognizing that these are preliminary observations—the specific problem definition (Foundation 2) will determine which characteristics truly matter.

**Key Principle from FSA:** "Architecture characteristics represent the definition of success for a system apart from its functionality" (FSA §4.1). Economic data systems must not only retrieve correct data but do so with appropriate performance, reliability, and security characteristics.

---

## Candidate Architecture Characteristics

### 1. **Availability** (Reliability Family)

**ISO Definition:** "Degree to which a system, product or component is operational and accessible when required for use" (FSA §4.2).

**Why It Matters in This Context:**

Economic data releases are **time-sensitive events** that move financial markets:

- **8:30 AM ET employment reports** can swing stock markets billions in minutes
- **FOMC announcements** regarding Fed Funds rate are scheduled, high-impact events
- **Quarterly GDP releases** affect policy and investment decisions

**Specific Implications:**

```
Critical Window Analysis:
- Employment Report: Friday 8:30 AM ET
- CPI Release: Mid-month ~8:30 AM ET  
- GDP Advance: Last week of month after quarter
- FOMC Decisions: Scheduled meeting days 2:00 PM ET

Downtime during these windows = missed business opportunities
```

**Candidate Problem Connection:**
- **Problem 1 (Financial Dashboard):** Requires 99.9%+ availability during market hours. A system down during jobs report release is worthless to traders.
- **Problem 2 (Revision Analyzer):** Lower availability requirements—batch analysis can tolerate occasional downtime.
- **Problem 5 (Business Newsletter):** Weekly cadence allows for maintenance windows; 99% availability sufficient.

**Architectural Decisions Implied:**
- May need redundant FRED API access paths
- Health monitoring and automatic failover
- Graceful degradation (show cached data if API unavailable)
- Maintenance windows must avoid market hours

**Measurement:** Uptime percentage, especially during critical release windows (8:00-9:00 AM ET weekdays).

---

### 2. **Performance Efficiency** (Time Behavior)

**ISO Definition:** "Measure of performance relative to amount of resources used under known conditions... includes time behavior (measure of response, processing times, and/or throughput rates)" (FSA §4.2).

**Why It Matters in This Context:**

Two distinct performance dimensions emerge:

**A. Response Time (Low Latency)**
- Financial markets react to data in **seconds**
- Delay in receiving employment data = missed trading opportunity
- Users expect "instant" dashboard updates

**B. Throughput (High Volume)**
- A revision analysis query might need thousands of vintage observations
- Regional dashboard might aggregate data across 50 states, 20 indicators
- Newsletter generation processes millions of data points weekly

**Specific Examples:**

```python
# Scenario 1: Real-time alert (Problem 1)
Target: < 60 seconds from FRED update to user notification
  - FRED API call: < 500ms
  - Data processing: < 5 seconds
  - Alert delivery: < 10 seconds
  - Total budget: 60 seconds
  
# Scenario 2: Historical analysis (Problem 2)
Target: Complete analysis in < 5 minutes for any recession period
  - Query 1,000 vintage observations for GDP
  - Calculate revision statistics  
  - Generate visualizations
  - If serial API calls: 1,000 × 500ms = 8+ minutes (TOO SLOW)
  - Need: Parallel fetching or bulk API access
  
# Scenario 3: Dashboard rendering (Problem 3)
Target: < 2 seconds to display regional comparison
  - 3 geographic levels (MSA, State, National)
  - 10 indicators per level
  - 12 months of data per indicator
  - 360 data points to retrieve and render
```

**Architectural Decisions Implied:**
- Aggressive caching strategy (data doesn't change retroactively, except revisions)
- Pre-computation of common aggregations (YoY changes, moving averages)
- Async/parallel API calls where possible
- Consider bulk download vs. individual series queries

**Tensions:**
- Caching improves performance but risks serving stale data during releases
- Pre-computation speeds queries but increases storage and processing costs

**Measurement:** 
- P95 response time for real-time queries
- Time to complete batch analysis jobs
- Dashboard initial load time

---

### 3. **Reliability** (Fault Tolerance & Recoverability)

**ISO Definition:** "Degree to which system functions under specified conditions for specified period... includes fault tolerance (does the software operate as intended despite hardware or software faults)" (FSA §4.2).

**Why It Matters in This Context:**

Economic data systems must handle **external service failures gracefully**:

**Failure Scenarios:**

1. **FRED API Temporarily Unavailable**
   - Network partition
   - FRED maintenance window
   - Rate limit exceeded
   - DNS resolution failure

2. **Malformed or Missing Data**
   - Series returns `null` values unexpectedly
   - API format changes (rare but possible)
   - Data embargo (series temporarily withheld)

3. **Downstream Service Failures**
   - Database connection lost
   - Cache service (Redis) crashes
   - Email delivery fails (for newsletter)
   - Alert notification service down

**Specific Implications:**

```python
# Example: Handling FRED API failure
try:
    current_data = fred_client.get_series("UNRATE", limit=1)
except APIUnavailableError:
    # Option A: Serve cached data with staleness warning
    current_data = cache.get("UNRATE:latest")
    warnings.append("Data may be stale (cache from 2 hours ago)")
    
except RateLimitError:
    # Option B: Exponential backoff and retry
    time.sleep(exponential_backoff(attempt))
    retry()
    
except MalformedDataError:
    # Option C: Graceful degradation
    log_error(series_id="UNRATE", error=e)
    return SeriesUnavailable(series_id="UNRATE", reason="data_quality")
```

**Candidate Problem Connection:**
- **Problem 1 (Financial Dashboard):** Critical—must never crash; degraded service better than no service
- **Problem 2 (Revision Analyzer):** Moderate—can retry failed queries; user can tolerate delays
- **Problem 4 (Educational Tool):** Lower—working with historical data; real-time reliability less critical

**Architectural Decisions Implied:**
- Circuit breaker pattern for FRED API calls
- Multi-level caching (memory, disk, database)
- Retry logic with exponential backoff
- Fallback data sources (if available)
- Graceful degradation strategies

**Recoverability Considerations:**
- Can system resume after crash without data loss?
- If processing 1,000 series in batch, can it checkpoint and resume?
- Is audit trail maintained for financial compliance?

**Measurement:**
- Mean time between failures (MTBF)
- Mean time to recovery (MTTR)
- Percentage of requests succeeding vs. falling back to cache

---

### 4. **Accuracy/Correctness** (Functional Correctness - Data Integrity)

**ISO Definition:** "Degree to which a product or system provides correct results with needed degree of precision" (FSA §4.2, Functional Correctness).

**Why It Matters in This Context:**

Economic data accuracy is **paramount**—incorrect data can lead to:
- Bad investment decisions (financial losses)
- Flawed policy analysis (wrong conclusions)
- Regulatory violations (if used for compliance)

**Specific Challenges:**

**A. Revision Handling (Bi-Temporal Accuracy)**

```python
# Challenge: Which "GDP" value is correct?
GDP Q1 2024:
  - April 30, 2024:  $27,620.5B  (advance estimate)
  - May 30, 2024:    $27,632.1B  (second estimate) 
  - June 27, 2024:   $27,645.3B  (third estimate)
  - July 15, 2025:   $27,673.2B  (annual revision)

# All are "correct" for their vintage date
# But system must track: "What was GDP on 2024-05-01?" → $27,620.5B (what was known then)
#                    vs: "What is GDP for Q1 2024?" → $27,673.2B (latest revision)
```

**B. Calculation Accuracy**

```python
# Year-over-year percentage change calculation
# Must handle: missing values, revision timing, precision

def calculate_yoy_change(series: Series, date: datetime) -> float:
    current = series.get_value(date)  
    year_ago = series.get_value(date - timedelta(days=365))
    
    # Edge cases:
    # - What if year_ago is None? (series started mid-year)
    # - What if current is revised but year_ago isn't yet?
    # - Rounding: 3.724% or 3.72% or 3.7%?
    # - Leap years: 365 or 366 days?
```

**C. Aggregation Correctness**

```python
# Regional aggregation
# Texas unemployment = weighted average of metro areas?
# Or is state value independently calculated?
# Summing components vs. using published aggregate

# Example: Do sub-regions sum to state total?
austin_unemployed + dallas_unemployed + houston_unemployed 
  ≠ texas_total_unemployed  
  
# Why? Different survey methodologies at different levels
# Must use published totals, not calculate from parts
```

**Candidate Problem Connection:**
- **Problem 1 (Financial Dashboard):** Critical—wrong data = wrong trades = financial loss
- **Problem 2 (Revision Analyzer):** Essential—the entire point is tracking correct vintages
- **Problem 4 (Educational Tool):** Important but not life-critical—pedagogical use case

**Architectural Decisions Implied:**
- **Immutable data store** for historical observations (append-only)
- **Explicit vintage tracking** (never update in place; add new vintage)
- **Checksums or data validation** on API responses
- **Audit trail** for all data transformations
- **Test suite** with known-good calculation examples
- **Rounding policies** documented and enforced

**Verification Strategies:**
- Compare calculated aggregates against published totals
- Regression tests with historical data
- Manual spot-checks of critical series
- Cross-reference with other data sources (Bloomberg, BEA)

**Measurement:**
- Data validation error rate
- Number of calculation discrepancies detected
- User-reported data quality issues

---

### 5. **Data Freshness** (Custom Characteristic - Time Behavior)

**Why This Needs Special Consideration:**

While **performance** measures how fast the system responds, **data freshness** measures how current the data is. These are distinct concerns for economic data:

```
System Performance: 100ms API response time ✓
Data Freshness: But showing data from yesterday ✗

Scenario: 
- 8:30 AM: BLS publishes employment data
- 8:31 AM: FRED API updates
- 8:45 AM: User queries dashboard → sees data from 8:29 AM

Fast system, stale data = problem
```

**Why It Matters in This Context:**

Different use cases have different freshness requirements:

| Use Case | Freshness Requirement | Rationale |
|----------|----------------------|-----------|
| **Financial trading** | < 1 minute | Markets move on new data |
| **Policy dashboard** | < 1 hour | Same-day awareness sufficient |
| **Monthly newsletter** | < 1 week | Summarizing recent trends |
| **Historical analysis** | N/A | Working with years-old data |

**Architectural Challenges:**

**A. Update Frequency Varies by Series**

```python
# Different series, different update schedules
Series          Frequency    FRED Update Lag
-------         ---------    ---------------
FEDFUNDS        Daily        T+1 day (next business day)
UNRATE          Monthly      First Friday 8:30 AM
GDP             Quarterly    ~30 days after quarter end
Annual Deficit  Yearly       Fiscal year closes → 1 month later

# How to know when to check for updates?
# Polling every minute wastes API calls for quarterly series
# Checking quarterly series weekly risks missing releases
```

**B. Release Calendar Complexity**

```python
# FRED doesn't provide "notify me when updated"
# Must either:
# 1. Poll frequently (wasteful)
# 2. Know release schedules (requires external calendar)
# 3. Detect staleness heuristically

def is_data_fresh(series: Series) -> bool:
    if series.frequency == "Daily":
        return series.last_updated > yesterday()
    elif series.frequency == "Monthly":
        # Expected: first Friday of month
        # But what if there's a delay or holiday?
        return series.last_updated > expected_release_date(series)
```

**Architectural Decisions Implied:**
- **Release calendar integration** (know when to expect updates)
- **Smart polling** (check daily series daily, quarterly series monthly)
- **Staleness detection** (flag when data is older than expected)
- **Cache invalidation strategy** (expire cache based on release schedule)
- **Last-update timestamps** (show users data age)

**Tensions:**
- More frequent polling = fresher data but higher API load
- Aggressive caching = better performance but staleness risk
- Real-time updates = complex infrastructure vs. batch = simpler but delayed

**Measurement:**
- Data lag: time from FRED update to system availability
- Staleness incidents: times when system showed outdated data during critical windows
- Update latency by series frequency

---

### 6. **Security** (Confidentiality & Accountability)

**ISO Definition:** "Degree to which software protects information and data... includes confidentiality (data accessible only to authorized), integrity (prevents unauthorized modification), accountability (can user actions be traced), and authenticity (proving identity)" (FSA §4.2).

**Why It Matters in This Context:**

At first glance, FRED data is **public** (anyone can access it), so security seems less critical. However:

**A. API Key Protection**

```python
# FRED API key in .env file
FRED_API_KEY=1aa332710f09f700ab1f946f1ae9376e

# Risks:
# - Committed to Git repository (leak to public)
# - Exposed in client-side code (browser dev tools)
# - Logged in plain text (application logs)
# - Shared across team (who used the key when?)

# If key is compromised:
# - Unauthorized usage against my quota
# - Rate limits affect legitimate requests
# - Tracking/attribution broken
```

**B. Derived Data Confidentiality**

```python
# Example: Proprietary analysis
# - Raw FRED data is public
# - But custom indicators/models may be trade secrets
# - "Our recession prediction model says..."

# Scenario: Financial firm builds proprietary model
# Must protect:
# - Model parameters/weights
# - Trading signals derived from public data
# - Client portfolios correlated with economic indicators
```

**C. User Data Protection**

```python
# Problem 3 (Regional Dashboard) for municipalities:
# - Which economic indicators is City X monitoring?
# - What thresholds trigger their policy decisions?
# - Who in city government accessed what data when?

# This metadata may be sensitive even if underlying data is public
```

**D. Audit and Accountability**

```python
# Financial services use case (Problem 1):
# Regulatory requirement: demonstrate what data was used for trades

# Audit log must show:
audit_entry = {
    "timestamp": "2024-03-15T08:31:42Z",
    "user": "trader_alice",
    "action": "query_series",
    "series_id": "UNRATE",
    "vintage": "2024-03-15",  # data as of this date
    "value": 3.8,
    "used_for": "trade_decision_XYZ"
}

# Years later: "Why did we make that trade?"
# Must be able to reconstruct: "Based on unemployment data of 3.8% 
# available at 8:31 AM on March 15, 2024"
```

**Architectural Decisions Implied:**
- **Secrets management** (never commit API keys; use environment variables or vault)
- **Access control** (who can query what data? who can see proprietary models?)
- **Audit logging** (immutable record of all data access)
- **Data provenance tracking** (where did this number come from?)
- **Encryption** (for derived/proprietary data, not raw FRED data)

**Candidate Problem Connection:**
- **Problem 1 (Financial Dashboard):** High—regulatory compliance requires audit trails
- **Problem 2 (Revision Analyzer):** Low-Moderate—academic use, but need to track sources
- **Problem 5 (Business Newsletter):** Low—informational content, minimal security needs

**Measurement:**
- Zero API key leaks to version control
- 100% audit coverage for financial use cases
- Time to detect/respond to unauthorized access

---

### 7. **Testability** (Maintainability Family)

**ISO Definition:** "How easily developers and others can test the software" (FSA §4.2, Maintainability).

**Why It Matters in This Context:**

Economic data systems have **unique testing challenges**:

**A. External Dependency Testing**

```python
# Challenge: How do you test FRED API integration?

# Problem: Can't control FRED's responses
def test_get_unemployment_rate():
    client = FREDClient(api_key=TEST_KEY)
    unrate = client.get_series("UNRATE", limit=1)
    
    # What assertions can we make?
    assert unrate.latest_value == ???  # Changes monthly!
    assert unrate.frequency == "Monthly"  # This is stable
    assert len(unrate.observations) > 0  # Probably safe
    
# Need: Mock/stub FRED responses for deterministic testing
```

**B. Time-Dependent Testing**

```python
# Challenge: Code behaves differently based on calendar

def should_update_series(series: Series) -> bool:
    """Should we check FRED for updates to this series?"""
    if series.frequency == "Monthly":
        # Check on first Friday of month
        return is_first_friday() and not updated_today(series)
    elif series.frequency == "Quarterly":
        # Check ~30 days after quarter end
        return days_since_quarter_end() >= 30
        
# How do you test "is_first_friday()" without waiting for first Friday?
# Need: Time mocking/dependency injection
```

**C. Data Quality Testing**

```python
# Challenge: Detecting data anomalies

def validate_observation(series: Series, obs: Observation) -> bool:
    """Is this observation reasonable?"""
    # Unemployment rate should be 0-25%
    # But in 2020 it hit 14.8% (unprecedented)
    # Static rules break; need adaptive thresholds
    
    if series.id == "UNRATE":
        if obs.value < 0 or obs.value > 25:
            return False  # Clearly wrong
        # But is 14.8% wrong or COVID shock?
        
# Need: Historical bounds, outlier detection, manual review flags
```

**D. Revision Testing**

```python
# Challenge: Testing bi-temporal correctness

def test_vintage_consistency():
    """GDP for Q1 2024 on May 1 should match advance estimate"""
    gdp = client.get_series(
        "GDP", 
        observation_start="2024-01-01",
        observation_end="2024-03-31",
        vintage_dates="2024-05-01"
    )
    
    # Need: Known-good vintage data for comparison
    # FRED doesn't guarantee vintages won't be re-revised retroactively
    # Edge case: What if methodology changed?
```

**Architectural Decisions Implied:**
- **Comprehensive mocking layer** (FakeREDClient for tests)
- **Test data fixtures** (known-good FRED responses captured)
- **Time abstraction** (injectable clock for date-dependent logic)
- **Property-based testing** (generate scenarios, check invariants)
- **Integration test suite** (against real FRED API, run nightly)
- **Regression test database** (known calculations to verify)

**Testing Strategy:**

```python
# Unit tests: Mock FRED API, test business logic
# Integration tests: Real FRED API (limited, in CI/CD)
# Contract tests: Verify our assumptions about FRED API format
# Data quality tests: Validate retrieved data meets expectations
```

**Tensions:**
- **Speed vs. Realism:** Mocked tests are fast but may not catch API changes
- **Cost vs. Coverage:** Real API tests consume rate limits
- **Determinism vs. Freshness:** Test fixtures become stale

**Measurement:**
- Test coverage percentage
- Time to run full test suite
- Number of false positives (tests fail but code is correct)
- API compatibility breakage detection time

---

## Anticipated Tensions and Trade-offs

Following FSA §4.3's guidance that "architecture is the stuff you can't Google the answer to," these trade-offs require project-specific decisions:

### Tension 1: **Availability vs. Data Freshness**

**The Conflict:**
- **High availability** → Aggressive caching, serve stale data if FRED is down
- **Data freshness** → Frequent API calls, cache invalidation, more failure points

**Specific Scenario:**
```
8:30 AM: Jobs report released
8:31 AM: FRED API updates
8:32 AM: Our system queries FRED → API timeout (high load)

Option A (Prioritize Availability):
  → Serve cached data from 8:29 AM
  → User sees stale data but system works
  → Financial trader makes decision on old data (bad outcome)

Option B (Prioritize Freshness):  
  → Retry FRED API until success
  → User waits 30 seconds
  → Dashboard appears "broken" (bad user experience)

Option C (Balanced):
  → Show cached data immediately with "UPDATING..." indicator
  → Poll FRED API in background
  → Update UI when fresh data arrives (optimistic UI pattern)
```

**Questions to Resolve:**
- What's worse: stale data or no data?
- Can we quantify staleness tolerance by use case?
- Should financial use cases have different SLAs than educational?

---

### Tension 2: **Performance (Speed) vs. Accuracy (Correctness)**

**The Conflict:**
- **Fast performance** → Pre-compute aggregations, cache calculations
- **Accuracy** → Recalculate on every request, handle revisions precisely

**Specific Scenario:**
```python
# Pre-computed approach (fast but accuracy risk)
dashboard_metrics = {
    "unemployment_yoy_change": 0.8,  # Calculated last night
    "gdp_growth_rate": 2.4,           # From yesterday
    "inflation_12mo_avg": 3.2         # Cached value
}
# Render time: 50ms ✓
# But what if GDP was revised this morning? ✗

# On-demand calculation (accurate but slow)
def get_dashboard():
    unrate = fetch_series("UNRATE")
    unrate_yoy = calculate_yoy(unrate)  # 500ms API call + calc
    
    gdp = fetch_series("GDP")
    gdp_growth = calculate_growth(gdp)  # 500ms API call + calc
    
    # Total: 2+ seconds per dashboard load ✗
    # But always correct, including today's revisions ✓
```

**Design Question:**
Do we accept that some dashboards show "eventually consistent" data, or mandate strict correctness at performance cost?

---

### Tension 3: **Testability vs. Simplicity**

**The Conflict:**
- **High testability** → Dependency injection, interfaces, mocking layers (complex)
- **Simplicity** → Direct FRED API calls, straightforward code (hard to test)

**Specific Scenario:**
```python
# Simple but hard to test
def get_unemployment():
    client = FREDClient(api_key=os.getenv("FRED_API_KEY"))
    return client.get_series("UNRATE")
    # How do you unit test this without hitting real API?

# Testable but more complex
class EconomicDataService:
    def __init__(self, data_source: DataSource):  # Dependency injection
        self.data_source = data_source
    
    def get_unemployment(self):
        return self.data_source.fetch_series("UNRATE")

# Now can inject FakeDataSource for tests
# But added abstraction layer, interfaces, more moving parts
```

**Trade-off:**
- Early project: favor simplicity, get working quickly
- Production system: favor testability, technical debt will compound
- Educational project: where on spectrum?

---

### Tension 4: **Security (Audit Logging) vs. Performance**

**The Conflict:**
- **Comprehensive auditing** → Log every query, every data access (I/O overhead)
- **High performance** → Minimize writes, keep system fast

**Specific Scenario:**
```python
# Heavy auditing (complete but slow)
def fetch_series(series_id: str, user: User):
    start = time.now()
    data = fred_api.get_series(series_id)
    end = time.now()
    
    audit_log.write({
        "user": user.id,
        "action": "fetch_series", 
        "series": series_id,
        "timestamp": start,
        "duration_ms": (end - start),
        "data_vintage": data.last_updated,
        "result_count": len(data.observations)
    })  # Disk I/O adds 50-100ms per query
    
    return data

# Minimal logging (fast but compliance risk)
def fetch_series(series_id: str):
    return fred_api.get_series(series_id)
    # 500ms per query vs 600ms with logging
    # But can't prove what data was used when
```

**Questions:**
- Is 10-20% performance penalty acceptable for compliance?
- Can we batch audit writes (fast but lose real-time visibility)?
- Which use cases require auditing vs. which don't?

---

### Tension 5: **Reliability (Fault Tolerance) vs. Simplicity**

**The Conflict:**
- **High reliability** → Circuit breakers, retries, fallbacks, health checks (complex)
- **Simple architecture** → Direct dependencies, fail fast (fragile)

**Specific Scenario:**
```python
# Simple but fragile
def get_data():
    return fred_api.get_series("GDP")
    # If FRED is down → immediate exception → 500 error to user

# Reliable but complex
def get_data():
    # Try primary source
    try:
        return fred_api.get_series("GDP")
    except APIError:
        # Fallback to cache
        try:
            return cache.get("GDP:latest")
        except CacheError:
            # Fallback to database
            try:
                return db.get_latest("GDP")
            except DBError:
                # Fallback to static snapshot
                return emergency_data.get("GDP")
                
    # Each fallback adds code, tests, failure modes
```

**Trade-off:**
How many layers of redundancy before system becomes unmaintainable?

---

## What I Don't Know Yet

These characteristics matter but can't be fully assessed without a concrete problem definition:

### 1. **Scalability** (Performance - Capacity)

**What I Don't Know:**
- How many concurrent users?
- Peak query volume during release windows?
- Data growth rate (new series added, historical backfill)?

**Why It Matters:**
- **Problem 1 (Financial Dashboard):** Could serve 1,000 traders simultaneously at 8:30 AM
- **Problem 4 (Educational Tool):** Probably < 100 concurrent students
- **Very different architectural requirements**

**Can't Assess Until:**
- Define specific user base size
- Understand concurrent access patterns
- Model data volume growth

---

### 2. **Interoperability** (Compatibility Family)

**What I Don't Know:**
- Will this system need to integrate with other economic data sources (World Bank, IMF, BEA directly)?
- Must it export data in specific formats (Excel, Tableau, PowerBI)?
- Does it need to feed into existing enterprise systems (ERP, BI tools)?

**Why It Matters:**
- **If standalone tool:** Can use FRED's native formats
- **If enterprise integration:** May need complex ETL pipelines, format transformations

**Can't Assess Until:**
- Understand deployment context
- Know about existing tool ecosystem
- Identify required integrations

---

### 3. **Usability** (Learnability & Operability)

**What I Don't Know:**
- Who are the end users? (Economists, traders, business owners, students?)
- What's their technical sophistication?
- What devices/platforms? (Web, mobile, desktop, API-only?)

**Why It Matters:**
- **Financial traders:** Need minimal UI, maximum data density, Bloomberg terminal aesthetic
- **Small business owners:** Need simplified visualization, plain English explanations
- **Students:** Need educational scaffolding, glossary, examples

**Can't Assess Until:**
- Define user personas
- Conduct user research
- Understand usage context (office vs. mobile vs. classroom)

---

### 4. **Deployability** (Portability - Installability)

**What I Don't Know:**
- Is this a SaaS service, on-premises deployment, or desktop application?
- What infrastructure is available? (Cloud, containers, bare metal?)
- Who manages deployment? (DevOps team, individual users, IT department?)

**Why It Matters:**
- **SaaS:** Focus on cloud scalability, multi-tenancy
- **On-premises:** Focus on easy installation, minimal dependencies
- **Desktop app:** Focus on cross-platform compatibility

**Can't Assess Until:**
- Understand deployment constraints
- Know about operational environment
- Identify who manages infrastructure

---

### 5. **Modifiability** (Maintainability Family)

**What I Don't Know:**
- Is this a one-semester academic project or long-term production system?
- Will others maintain this code?
- How often will requirements change?

**Why It Matters:**
- **Short-term project:** Can take shortcuts, prioritize speed
- **Long-term system:** Must invest in documentation, modularity, extensibility

**Can't Assess Until:**
- Clarify project lifespan expectations
- Understand maintenance handoff requirements
- Know about future enhancement plans

---

## Preliminary Characteristic Priorities

Based on candidate problems and domain observations, **tentative importance ranking**:

| Rank | Characteristic | Why Critical |
|------|---------------|--------------|
| 1 | **Accuracy/Correctness** | Wrong economic data = wrong decisions (universal requirement) |
| 2 | **Availability** | Especially for financial use cases; less critical for batch analysis |
| 3 | **Data Freshness** | Time-sensitive nature of economic releases |
| 4 | **Reliability** | Must handle FRED API failures gracefully |
| 5 | **Performance** | Important but secondary to correctness |
| 6 | **Testability** | Essential for verifying correctness, preventing regressions |
| 7 | **Security** | Matters for financial/enterprise use; less for educational |

**Characteristics NOT Prioritized (Yet):**
- **Scalability:** Unknown until user base defined
- **Usability:** Problem-dependent (traders vs. students)
- **Portability:** Deployment model unclear
- **Modifiability:** Project lifespan uncertain

**Key Insight from FSA §4.4:** "Never shoot for generic reusability; it is a myth. Instead, shoot for specificity, which can lead to reusability."

---

## Connections to FSA Chapters 4-5

### Chapter 4 Concepts Applied:

**§4.1 Architecture Characteristics (Partially) Listed:**
- Analyzed characteristics from ISO standard (Performance, Reliability, Security, Maintainability)
- Identified domain-specific characteristics (Data Freshness)
- Recognized that characteristics often conflict

**§4.2 Operational Architecture Characteristics:**
- **Availability:** Critical during market hours
- **Performance/Efficiency:** Low latency for real-time; high throughput for batch
- **Reliability:** Fault tolerance for external API
- **Scalability:** Deferred until problem definition

**§4.3 Structural Architecture Characteristics:**
- **Testability:** External dependency challenges
- **Maintainability:** Project lifespan uncertain
- **Modifiability:** Requirements volatility unknown

**§4.4 Trade-offs and Tensions:**
- Availability vs. Freshness
- Performance vs. Accuracy  
- Testability vs. Simplicity
- Security vs. Performance
- Reliability vs. Simplicity

### Chapter 5 Concepts Applied:

**§5.1 Extracting Architecture Characteristics:**
Following the guidance to "listen for clues in domain descriptions":
- **"Time-sensitive releases"** → Availability, Performance, Freshness
- **"Financial decisions"** → Accuracy, Security (audit trails)
- **"Revisions over time"** → Data integrity, testability challenges
- **"External API dependency"** → Reliability, fault tolerance

**§5.2 Prioritizing Characteristics:**
- Recognized that correctness is non-negotiable (domain constraint)
- Identified that other priorities depend on specific problem (Problem 1 ≠ Problem 4)
- Acknowledged trade-offs require project-specific decisions

---

## Next Steps for Foundation 2

When defining the specific problem, I must:

1. **Quantify characteristic requirements** (not just "fast" but "< 100ms P95")
2. **Prioritize conflicting characteristics** (which trade-off to make?)
3. **Define success metrics** (how will we measure if we achieved the characteristic?)
4. **Eliminate irrelevant characteristics** (don't design for scalability if max users = 10)
5. **Document architectural decisions** (why we chose availability over freshness)

**FSA Principle:** "The architecture characteristics you select define the constraints and considerations for architectural decisions" (§4.1).

---

**Repository:** `Foundation-1-Zane-Hill` branch  
**Related Files:**
- `Dataset_Selection_Justification.md` - Dataset context
- `Initial_Problem_Space.md` - Problem discovery
- `FRED_Data_Retrieval.py` - Working implementation showing technical constraints
