# Kata 5: Concurrent Data Fetching

## Overview

This project demonstrates **concurrent data fetching** using Python's `ThreadPoolExecutor`. The script fetches economic data from the **FRED (Federal Reserve Economic Data) API** for multiple series simultaneously, rather than sequentially.

## Key Concepts

### What is Concurrency?

**Concurrency** means doing multiple tasks at the same time. In this project:
- **Without concurrency (Serial):** Fetch series 1 → wait → Fetch series 2 → wait → Fetch series 3 → wait
- **With concurrency (Parallel):** Fetch series 1, 2, 3 **at the same time**

### ThreadPoolExecutor

A **thread pool** is a collection of worker threads that execute tasks from a queue. Benefits:
- **Manages threads automatically** — No need to manually create/destroy threads
- **Limits resource usage** — Only creates a fixed number of workers (e.g., 3)
- **Simple API** — Call `executor.submit(function, args)` to queue a task

Example:
```python
with ThreadPoolExecutor(max_workers=3) as executor:
    # Submit 4 tasks, executed across 3 workers
    futures = [
        executor.submit(fetch_series, "CPIAUCSL", api_key, timeout),
        executor.submit(fetch_series, "FEDFUNDS", api_key, timeout),
        executor.submit(fetch_series, "IPG3344S", api_key, timeout),
        executor.submit(fetch_series, "UMCSENT", api_key, timeout),
    ]
    
    # Collect results as they complete
    for future in futures:
        series_id, result = future.result()
```

### Thread Safety

When multiple threads access the same resource (e.g., a file), **race conditions** can occur. A **Lock** prevents this:

```python
write_lock = threading.Lock()

with write_lock:
    # Only ONE thread executes this block at a time
    file.write(data)  # Safe!
```

## Project Structure

```
Kata5/
├── concurrent_fetch.py      # Main script with threading logic
├── config.json              # Configuration: series list, pool size, timeout
├── README.md                # This file
├── results/                 # Output directory for successful fetches
│   └── combined_results.json
└── logs/                    # Error logging
    └── errors.log
```

## How to Run

### Prerequisites

- Python 3.7+
- `requests` library
- `python-dotenv` library
- FRED API key in `.env` file (parent directory)

### Execution

```bash
# Navigate to Kata5 directory
cd CIDM6330/Katas/Kata5

# Run the script
python concurrent_fetch.py
```

### Configuration

Edit `config.json` to control behavior:

```json
{
  "pool_size": 3,              // Number of worker threads
  "timeout": 10,              // Request timeout in seconds
  "series": [                 // FRED series to fetch
    "CPIAUCSL",               // Consumer Price Index
    "FEDFUNDS",               // Federal Funds Rate
    "IPG3344S",               // Industrial Production
    "UMCSENT"                 // Consumer Sentiment
  ]
}
```

## Output

### Success Output

```
Fetching all series concurrently...

==================================================
RESULTS:
==================================================

CPIAUCSL:
  ✓ SUCCESS: 949 observations

FEDFUNDS:
  ✓ SUCCESS: 860 observations

IPG3344S:
  ✓ SUCCESS: 649 observations

UMCSENT:
  ✓ SUCCESS: 879 observations

==================================================
WRITING TO FILES:
==================================================
✓ Wrote 4 successful series to results/combined_results.json
✓ No errors encountered!
```

### Results File

`results/combined_results.json` contains fetched data structured as:

```json
{
  "CPIAUCSL": [
    {"date": "1947-01-01", "value": "21.48", ...},
    {"date": "1947-02-01", "value": "21.48", ...}
  ],
  "FEDFUNDS": [
    {"date": "1954-08-01", "value": "1.13", ...}
  ]
}
```

### Error Handling

If any fetch fails, errors are logged to `logs/errors.log`:

```
INVALID_SERIES_ID_XYZ: HTTP error for INVALID_SERIES_ID_XYZ: 400
```

## Performance Benefits

**Example timing:**
- **Serial execution:** 4 requests × 1 second each = **4 seconds**
- **Concurrent execution (3 workers):** ~1.33 seconds (**3x faster**)

Larger numbers of parallel requests see greater speedup. Network I/O (waiting for API responses) is where concurrency shines—threads don't block each other.

## Key Learning Points

1. **ThreadPoolExecutor** simplifies concurrent programming
2. **Locks** are essential for thread-safe file operations
3. **Error handling** must gracefully manage individual failures
4. **Configuration files** make code reusable and testable

## Git Workflow

This project was developed with frequent, meaningful commits:

```
Phase 1: Single-threaded fetcher with error handling
Phase 2: Add ThreadPoolExecutor for concurrent fetching
Phase 3: Add thread-safe file writing for results and error logs
```

## Future Enhancements

- **Async/Await:** Compare performance with `asyncio` implementation
- **Retry logic:** Automatically retry failed requests
- **Caching:** Cache results to avoid redundant API calls
- **Progress bar:** Display real-time fetch progress
