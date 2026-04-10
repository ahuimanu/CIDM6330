# Distributed Considerations — Foundation 3

## Current State: Monolithic Pipeline

The Shortage Scout is a single-process, single-machine pipeline. Running `python run_pipeline.py` executes all stages — acquire, normalize, aggregate, calculate, output — sequentially within one Python process. There is no network communication between components, no message broker, no separate services.

---

## Why I Chose Not to Distribute

The decision to stay monolithic was deliberate, not accidental.

**The problem shape is inherently sequential.** Each stage depends entirely on the output of the previous one. The rolling average cannot run until percent-change normalization is complete. The S_score cannot be calculated until the rolling average exists. There is no work that can be parallelized across the four stages — they form a strict dependency chain.

**The data volume does not justify distribution.** This pipeline processes four monthly FRED time series. The largest realistic dataset covers ~40 years of monthly data = ~480 rows × 4 columns. This fits in memory in milliseconds. A distributed system adds network latency, serialization overhead, and deployment complexity to a problem that completes in under 5 seconds on a laptop.

**The failure model for distribution is worse.** The Foundation 2 architecture decision explicitly accepted "loud failure" (pipeline crash) over "silent failure" (bad math that passes through). Distributing the mathematical stages across services introduces partial-failure scenarios: the normalization service could succeed while the aggregation service times out, leaving the system in an inconsistent intermediate state. A monolith either runs to completion or crashes cleanly.

**Cost.** This is a monthly batch job. Running it once per month on a developer's machine or a free GitHub Actions runner costs effectively nothing. Deploying microservices costs something every hour, regardless of whether the pipeline ran.

---

## What I Would Gain by Distributing

If this system were to scale — say, expanding from 4 FRED series to 400, or running daily instead of monthly — the following distribution patterns become attractive:

**Fan-out acquisition:** Each FRED series fetch is independent. With 400 series, distributing acquisition across a worker pool (e.g., `concurrent.futures.ThreadPoolExecutor`) would reduce fetch time proportionally. This is parallelism within a process, not true distribution, but it addresses the bottleneck without adding network complexity.

**Separation of acquisition and transformation:** If FRED data needed to be archived for auditability (raw response archiving is the biggest current gap), a message queue (e.g., a simple file-system queue or AWS SQS) between the fetcher and the transformer would allow acquisition and transformation to scale independently and provide a durable record of what was fetched.

**Scheduled invocation as a service boundary:** Currently, `run_pipeline.py` is manually invoked. Wrapping it as a cron job (GitHub Actions schedule, or a cloud scheduler) creates a lightweight "trigger" boundary without requiring the pipeline itself to be distributed.

---

## Data Ownership

In the current monolithic design, data ownership is straightforward:

| Stage | Owns | Where |
|---|---|---|
| `acquire.py` | Raw FRED observations | `Foundation3/results/*.csv` |
| `transform.py` | Normalized metrics, S_score | In-memory DataFrame (not persisted separately) |
| `pipeline.py` | Final output payload | `Foundation3/results/transformed.json` |

**Truth lives in `transformed.json`.** The `combined.csv` preserves the raw inputs; `transformed.json` is the authoritative recommendation record. There is no shared mutable state between stages — each stage receives an input, produces an output, and does not modify previous stages' artifacts.

**If distributed:** The "who owns what" question becomes a data contract problem. Each service would need to agree on the schema of the DataFrame it receives and emits. The current function signatures (`fetch_all` returns `Dict[str, pd.Series]`; `transform_combined` takes a `pd.DataFrame`) are already typed contracts — they would translate directly to message schemas in a distributed design.
