# Kata 3 - API Consumption (FRED)

## What this kata does
- Fetches paginated results from the FRED observations endpoint using `limit` and `offset`
- Fetches a series such as GDP observations
- Implements retry logic with exponential backoff and jitter
- Handles transient HTTP errors and rate limits
- Writes output to JSON

## How to run
Set API key:
- PowerShell: `setx FRED_API_KEY "your_32_char_lowercase_key"`

Restart the terminal, then:

```bash
python -m pip install requests
python foundation-02/foundation-02/katas/kata-03-api/kata3_api_consume.py
```

## Kata 8 testing note
The Kata 8 test suite mocks `requests.get`, retries, and error handling so the tests work fully offline.
