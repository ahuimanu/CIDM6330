---
title: External Integrations
mapped: 2026-05-04
---

# External Integrations

## External APIs

### FRED (Federal Reserve Economic Data)
- **Provider:** Federal Reserve Bank of St. Louis
- **Auth:** API key via `FRED_API_KEY` environment variable (loaded from `.env`)
- **Usage:** `Foundation3/acquire.py` fetches economic time series data
- **Default series:**
  - `IPG3344S` — Industrial production: semiconductor manufacturing
  - `CAPUTLG3344SQ` — Capacity utilization: semiconductor manufacturing
  - `A34STI` — Manufacturers' shipments, inventories (electronics)
  - `PCU334413334413` — Producer price index: semiconductors
- **Retry logic:** Present in `Foundation3/acquire.py` with backoff
- **Fallback:** Demo mode (`run_pipeline.py --demo` or missing API key) uses `Foundation3/generate_sample.py` for synthetic data
- **Auditability:** Raw JSON payloads archived with vintage dates to `Foundation3/results/`

## Databases

### SQLite
- **Usage:** Kata2 exercises (`Katas/Kata2/`)
- **Access:** `sqlite3` stdlib + SQLAlchemy ORM
- **Pattern:** Ephemeral test databases via `tmp_sqlite_db` pytest fixture

### Redis
- **Usage:** Course exercises only (Celery broker, Django Channels layer)
- **Packages:** `redis==5.2.1`, `channels_redis==4.2.1`
- **Not used in production pipeline**

## Message Queues

### Celery (course exercise)
- **Broker:** Redis
- **Usage:** `django-celery-beat==2.7.0` for periodic task scheduling exercises
- **Not part of the Shortage Scout pipeline**

## Authentication

- No auth providers (OAuth, Auth0, etc.) present
- Only API key auth for FRED (`FRED_API_KEY`)

## Webhooks / Event Streams

- None present

## File I/O

- **Output directory:** `Foundation3/results/` — CSV and JSON outputs from pipeline runs
- **Archive pattern:** Raw FRED JSON saved with vintage date in filename for auditability

## External Services (course exercises only)

- Django REST Framework API endpoints (`djangorestframework`)
- FastAPI async endpoints
- Flask routes
- WebSocket via Django Channels + Redis
- These are separate course exercises, not connected to the main Shortage Scout pipeline
