Kata 3 — API Consumption
Foundation 2, Sprint Week 1

Python Focus: HTTP/Web APIs (Client)
Git Focus: Merge Conflicts
The Exercise:

Create a Python script that:

Fetches data from a public API (choose one: FRED, BLS, NOAA, or any from your dataset pool that has an API)
Handles pagination if the API returns paginated results
Implements retry logic with exponential backoff for failed requests
Saves the results to a local file (JSON or CSV)
Requirements:

Use the requests library
Handle HTTP errors appropriately (don't just crash on 4xx/5xx)
Respect rate limits (implement delay between requests if needed)
Use environment variables for API keys (never hardcode)
Git Tasks:

Create two branches from main that modify the same file differently
Practice resolving a merge conflict:
Create branch-a, modify the retry logic, commit
Switch to main, create branch-b, modify the same retry logic differently, commit
Merge branch-a to main
Merge branch-b to main (conflict!), resolve it
Document what you learned about conflict resolution in a commit message
Stretch:

Implement async requests using aiohttp for concurrent API calls