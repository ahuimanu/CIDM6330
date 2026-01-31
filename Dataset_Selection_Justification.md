# Dataset Selection Justification

**Student:** Zane Hill  
**Course:** CIDM 6330 - Software Architecture  
**Date:** January 31, 2026  
**Branch:** Foundation-1-Zane-Hill

---

## 1. Source and Scope

**Dataset:** Federal Reserve Economic Data (FRED)  
**Agency:** Federal Reserve Bank of St. Louis  
**API Version:** FRED API v1 and v2  
**URL:** https://fred.stlouisfed.org/ | https://fred.stlouisfed.org/docs/api/fred/

### Specific Data Collections

This project will work with multiple interconnected FRED datasets:

- **Economic Time Series Data**: 840,000+ economic indicators from 118 sources
  - GDP measurements (quarterly, annual)
  - Unemployment rates (monthly, national and regional)
  - Interest rates (daily, weekly, monthly)
  - Inflation indicators (CPI, PCE, various frequencies)
  - Exchange rates (daily)
  - Money supply aggregates (weekly, monthly)
  
- **ALFRED (Archival FRED)**: Point-in-time historical revisions
  - Vintage dates showing what was known when
  - Complete revision history for all series
  
- **Series Metadata**: Rich categorization and tagging system
  - Hierarchical category structure (8 top-level, 1000+ subcategories)
  - Release information linking series to source publications
  - Source agency metadata (BLS, BEA, Census Bureau, etc.)

### Data Coverage

- **Temporal Span**: 1776 to present (varies by series)
- **Geographic Scope**: National, state, MSA, and county-level data
- **Economic Sectors**: All major sectors (finance, employment, production, prices, etc.)

---

## 2. Access Verification

### API Access Confirmed

Successfully authenticated and retrieved data using FRED API key on January 31, 2026.

**API Endpoint:** `https://api.stlouisfed.org/fred/`  
**Authentication:** API key-based (32-character alpha-numeric string)  
**Data Format:** JSON, XML, CSV, Excel

### Sample API Response - GDP Series

```json
{
  "id": "GDP",
  "title": "Gross Domestic Product",
  "units": "Billions of Dollars",
  "frequency": "Quarterly",
  "seasonal_adjustment": "Seasonally Adjusted Annual Rate",
  "last_updated": "2026-01-22T07:46:34-06:00",
  "popularity": 95,
  "observations": [
    {
      "date": "1947-01-01",
      "value": "243.164",
      "realtime_start": "2026-01-31",
      "realtime_end": "2026-01-31"
    }
  ]
}
```

### Sample Retrieved Data

**Unemployment Rate (UNRATE) - Recent Observations:**
```
2020-01-01: 3.6%
2020-02-01: 3.5%
2020-03-01: 4.4%
2020-04-01: 14.8%  (COVID-19 impact)
2020-05-01: 13.2%
2020-06-01: 11.0%
2020-07-01: 10.2%
2020-08-01: 8.4%
2020-09-01: 7.8%
2020-10-01: 6.9%
```

**Federal Funds Rate (FEDFUNDS) - Historical Data:**
```
1954-07-01: 0.80%
1954-08-01: 1.22%
...
1955-06-01: 1.64%
```

### Series Search Capability

Successfully searched for "inflation" and retrieved 5 related series:
- DFII10: Market Yield on 10-Year Treasury (Inflation-Indexed)
- FII10: 10-Year Constant Maturity (Inflation-Indexed)
- T10YIE: 10-Year Breakeven Inflation Rate

### Category Browsing

Retrieved top-level categories:
- 32991: Money, Banking, & Finance
- 10: Population, Employment, & Labor Markets
- 32992: National Accounts
- 1: Production & Business Activity
- 32455: Prices
- 32263: International Data
- 3008: U.S. Regional Data
- 33060: Academic Data

### Data Persistence

Successfully saved data to local JSON files:
- `fred_data/GDP.json`
- `fred_data/UNRATE.json`
- `fred_data/FEDFUNDS.json`

**Access Status:** ✅ **Fully Operational** - No barriers encountered

---

## 3. Relational Depth

FRED provides extensive relational structure with multiple linkage points for complex queries and analysis.

### Primary Relationships

#### 1. **Series ↔ Categories** (Many-to-Many)

Each economic series belongs to one or more categories in a hierarchical taxonomy.

**Example:**
```
Series: UNRATE (Unemployment Rate)
  ├─ Category: Population, Employment, & Labor Markets (ID: 10)
  │   └─ Subcategory: Current Employment Statistics (ID: 12)
  │       └─ Subcategory: National Employment (ID: 11)
  └─ Category: National Accounts (ID: 32992)
```

**Join Relationship:**
```python
# Pseudocode for relationship
series.id → series_categories.series_id
series_categories.category_id → categories.id
categories.parent_id → categories.id  # Hierarchical
```

#### 2. **Series ↔ Releases** (Many-to-One)

Each series comes from a specific data release (publication), updated on a schedule.

**Example:**
```
Series: GDP
  └─ Release: Gross Domestic Product (ID: 53)
      ├─ Release Date: Quarterly (last Friday of month)
      ├─ Source: Bureau of Economic Analysis
      └─ Related Series: GDPC1, GDPDEF, GDPPOT (20+ series)

Series: UNRATE
  └─ Release: Employment Situation (ID: 50)
      ├─ Release Date: Monthly (first Friday)
      ├─ Source: Bureau of Labor Statistics
      └─ Related Series: PAYEMS, CIVPART, U6RATE (50+ series)
```

**Join Relationship:**
```python
series.id → release_series.series_id
release_series.release_id → releases.id
releases.source_id → sources.id
```

#### 3. **Series ↔ Observations (Vintage Dates)** (One-to-Many)

ALFRED provides revision history - the same observation point has multiple vintage values.

**Example:**
```
Series: GDP, Date: 2024-Q1
  ├─ Vintage 2024-04-30: $27,620.5 billion (advance estimate)
  ├─ Vintage 2024-05-30: $27,632.1 billion (second estimate)
  └─ Vintage 2024-06-27: $27,645.3 billion (third estimate)
```

**Join Relationship:**
```python
series.id → observations.series_id
observations.date + observations.realtime_start → unique vintage
```

#### 4. **Series ↔ Tags** (Many-to-Many)

Series are tagged with keywords for discovery and grouping.

**Example:**
```
Series: UNRATE
  Tags: [usa, unemployment, nsa, nation, bls, employment, monthly]

Series: GDP  
  Tags: [usa, gdp, nation, quarterly, nsa, bea, national accounts]
```

**Join Relationship:**
```python
series.id → series_tags.series_id
series_tags.tag_name → tags.name
tags.group_id → tag_groups.id
```

### Complex Multi-Table Queries

**Example Use Case:** Find all monthly employment indicators from BLS that were revised in the last quarter.

```sql
SELECT s.id, s.title, o.date, o.value, o.realtime_start
FROM series s
  JOIN release_series rs ON s.id = rs.series_id
  JOIN releases r ON rs.release_id = r.id
  JOIN sources src ON r.source_id = src.id
  JOIN observations o ON s.id = o.series_id
WHERE src.name = 'Bureau of Labor Statistics'
  AND s.frequency = 'Monthly'
  AND o.realtime_start >= '2025-10-01'
  AND s.id IN (
    SELECT series_id FROM series_tags WHERE tag_name = 'employment'
  );
```

### Architectural Implications

These relationships enable sophisticated architectural patterns:

- **Repository Pattern**: Separate repositories for Series, Observations, Categories, Releases
- **Unit of Work**: Coordinate changes across related entities (series + observations + vintages)
- **Lazy Loading**: Load observations only when needed (series metadata first)
- **Caching Strategy**: Cache series metadata but invalidate observations based on release schedules
- **Event Sourcing**: Use ALFRED vintage dates as natural event stream

---

## 4. Temporal Characteristics

### Update Frequency

FRED series have **varying update frequencies** based on source publication schedules:

| Frequency | Example Series | Update Schedule | Count |
|-----------|---------------|-----------------|-------|
| **Daily** | FEDFUNDS, DGS10, DEXUSEU | Business days, next day | ~1,000 |
| **Weekly** | M1, MORTGAGE30US, ICSA | Every Thursday | ~500 |
| **Monthly** | UNRATE, CPI, PAYEMS | First week of month | ~400,000 |
| **Quarterly** | GDP, GDPC1, PCE | End of quarter + 30 days | ~50,000 |
| **Annual** | FYFSD, GFDEGDQ188S | Once per year | ~100,000 |

**Real-Time Consideration:** Some series (like GDP) are revised multiple times after initial release. ALFRED tracks all revisions.

### Historical Depth

FRED contains one of the deepest economic time series archives:

| Series | Start Date | Data Points | Historical Significance |
|--------|------------|-------------|------------------------|
| **GDP** | 1947-01-01 | 300+ quarters | Post-WWII reconstruction onward |
| **FEDFUNDS** | 1954-07-01 | 850+ months | Federal Reserve era |
| **CPIAUCSL** | 1947-01-01 | 900+ months | Modern inflation tracking |
| **DGS10** | 1962-01-02 | 15,000+ days | Modern bond market |
| **UNRATE** | 1948-01-01 | 900+ months | Post-war labor markets |
| **M2** | 1959-01-01 | 750+ months | Money supply tracking |

**Observation Start Parameter:** API allows `observation_start="1776-07-04"` (symbolic default) to retrieve all available history.

### Time Granularity

#### Observation-Level Granularity
- **Daily**: Foreign exchange rates, treasury yields, fed funds rate
- **Weekly**: Money supply (M1, M2), mortgage rates, unemployment claims
- **Monthly**: Employment, CPI, retail sales, industrial production
- **Quarterly**: GDP, national income accounts, flow of funds
- **Annual**: Long-term fiscal data, international comparisons

#### Vintage-Level Granularity (ALFRED)

Every series maintains **point-in-time snapshots** showing data as it existed on any historical date:

```
What did GDP for 2023-Q2 look like on different dates?
  - 2023-07-27 (advance estimate): $26,840.7B
  - 2023-08-30 (second estimate):  $26,852.0B  
  - 2023-09-28 (third estimate):   $26,858.2B
  - 2024-01-25 (annual revision):  $26,873.1B
```

This enables:
- **Backtesting**: Test forecasting models with data as it existed historically
- **Revision Analysis**: Measure forecast vs. initial release vs. final value
- **Real-Time Simulation**: Reproduce economic analysis as it would have appeared at any point in history

### Release Schedules

Series follow predictable release patterns:

```python
# Example Release Schedule
Employment Situation (UNRATE, PAYEMS):
  - First Friday of every month at 8:30 AM ET
  - Covers previous month's data
  
GDP (Advance Estimate):
  - Last week of the month following quarter-end
  - Second estimate: +1 month
  - Third estimate: +2 months
  - Annual revisions: July of following year

CPI:
  - Mid-month (usually ~13th) at 8:30 AM ET
  - Covers previous month's data
```

**Architectural Consideration:** Applications can schedule data refreshes based on known release calendars, minimizing unnecessary API calls.

### Data Latency

| Update Type | Latency | Example |
|-------------|---------|---------|
| Real-time (daily) | T+1 day | Federal funds rate posted next business day |
| High-frequency (weekly) | T+3 days | Initial unemployment claims (Thursday for previous week) |
| Monthly indicators | T+2 to T+4 weeks | Employment (first Friday), CPI (mid-month) |
| Quarterly accounts | T+1 month | GDP advance estimate |
| Annual aggregates | T+6 to T+12 months | Fiscal year totals, census updates |

### Temporal Query Capabilities

API supports sophisticated temporal queries:

```python
# Get observations for specific date range
observations = client.get_series_observations(
    series_id="UNRATE",
    observation_start="2020-01-01",
    observation_end="2023-12-31"
)

# Get data as it existed on a specific historical date (ALFRED)
vintage_observations = client.get_series_observations(
    series_id="GDP",
    vintage_dates="2020-06-01,2021-06-01,2022-06-01"
)

# Get real-time window
realtime_observations = client.get_series_observations(
    series_id="GDPC1",
    realtime_start="2023-01-01",
    realtime_end="2023-12-31"
)
```

---

## 5. Why This Dataset

### Personal and Academic Interest

#### 1. **Architectural Complexity**

FRED presents fascinating architectural challenges that go beyond simple CRUD operations:

- **Time Series Storage**: How do you efficiently store and query millions of time-ordered observations?
- **Versioning/Revision Tracking**: ALFRED's vintage dates create a natural event-sourcing pattern
- **Caching Strategy**: Balance freshness with API rate limits given known release schedules
- **Materialized Views**: Pre-compute common aggregations (YoY changes, moving averages)
- **Data Consistency**: Handle late-arriving revisions without breaking downstream analytics

These are the kinds of **real-world architectural problems** that production systems face.

#### 2. **Real-World Relevance**

Economic data drives trillion-dollar decisions:
- Central banks use this data to set interest rates
- Investors use it for asset allocation
- Businesses use it for strategic planning
- Researchers use it to understand economic cycles

Working with **actual data that matters** is more motivating than toy datasets.

#### 3. **Clean, Well-Documented API**

The FRED API is exemplary in its design:
- **RESTful** principles properly applied
- **Comprehensive documentation** with examples
- **Stable** (Version 1 has been running since 2011)
- **Free tier** sufficient for academic work
- **Multiple client libraries** showing good adoption

This allows focus on **architecture** rather than fighting a poor API.

#### 4. **Temporal Data Patterns**

Time series data introduces unique architectural considerations:

- **Append-Only Nature**: Past observations don't change (except via revisions)
- **Predictable Access Patterns**: Recent data accessed far more than historical
- **Natural Partitioning**: Can partition by time periods (yearly, monthly)
- **Aggregation Queries**: "What was average inflation 2020-2023?" 
- **Sliding Window**: "Show me last 12 months of unemployment"

These patterns appear in **many domains**: IoT sensors, application logs, financial ticks, web analytics.

#### 5. **Multiple Integration Patterns**

FRED data can be consumed in various architectural styles:

- **Batch ETL**: Nightly pulls of updated series
- **Streaming**: Real-time updates as new data publishes
- **Request/Response**: On-demand queries from web app
- **Event-Driven**: Trigger notifications when key indicators change
- **Materialized Analytics**: Pre-computed dashboards and reports

This flexibility enables exploration of **multiple architectural approaches**.

#### 6. **Cross-Domain Learning**

Economics intersects with many fields:
- **Data Science**: Time series forecasting, anomaly detection
- **Statistics**: Regression analysis, hypothesis testing  
- **Visualization**: Charts, dashboards, interactive exploration
- **Domain Modeling**: Rich vocabulary (GDP, inflation, unemployment) requires thoughtful entity design

Building around economic data provides **context beyond pure software architecture**.

#### 7. **Personally Compelling Use Cases**

Several project directions interest me:

**A. Economic Indicator Dashboard**
- Real-time visualization of key indicators
- Historical comparisons across recession periods
- Alerting when metrics cross thresholds

**B. Revision Analysis System**  
- Track how GDP/employment estimates change over time
- Measure "surprise factor" of data releases
- Analyze which agencies revise most

**C. Regional Economic Comparison**
- Compare unemployment across states/metros
- Identify regional economic trends
- Correlate with migration patterns

**D. Time Series API Gateway**
- Unified interface to FRED + other economic APIs
- Rate limiting and caching layer
- Transformation and aggregation services

Any of these provides rich architectural exploration while working with **meaningful data**.

### Long-Term Sustainability

This dataset choice supports a semester-long project because:

- ✅ **Consistently Available**: FRED has 15+ year track record
- ✅ **Actively Maintained**: Data updated on regular schedules  
- ✅ **Growing Dataset**: New series added regularly
- ✅ **No Cost Barriers**: Free API with generous rate limits
- ✅ **Rich Documentation**: Comprehensive guides and examples
- ✅ **Community Support**: Wide user base (academics, finance, government)
- ✅ **Multiple Architectures**: Can build sync, async, batch, streaming systems
- ✅ **Clear Requirements**: Well-defined data model and relationships

---

## Conclusion

The Federal Reserve Economic Data (FRED) API provides an ideal foundation for exploring software architecture concepts:

1. ✅ **Verified Access**: Successfully authenticated and retrieved multiple series
2. ✅ **Rich Relational Structure**: Series, Categories, Releases, Sources, Tags, Vintages
3. ✅ **Deep Temporal Characteristics**: Daily to annual frequencies, decades of history, revision tracking
4. ✅ **Architectural Interest**: Time series patterns, caching strategies, event sourcing, materialized views
5. ✅ **Personal Motivation**: Real-world relevance, clean API, compelling use cases

This dataset will support meaningful architectural exploration throughout the semester while working with data that has genuine economic and social impact.

---

**Repository:** `Foundation-1-Zane-Hill` branch  
**Implementation:** `FRED_Data_Retrieval.py`  
**Data Directory:** `fred_data/`
