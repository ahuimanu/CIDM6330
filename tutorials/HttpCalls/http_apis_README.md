# HTTP and Web APIs in Python

This guide covers making HTTP requests and consuming web APIs in Python. We progress through three approaches: the stdlib `urllib`, the popular `requests` library, and the modern `httpx` library with async support.

## Table of Contents

1. [HTTP Fundamentals](#http-fundamentals)
2. [urllib: The Standard Library](#urllib-the-standard-library)
3. [requests: The Ergonomic Standard](#requests-the-ergonomic-standard)
4. [httpx: Modern Async-Capable HTTP](#httpx-modern-async-capable-http)
5. [Working with JSON APIs](#working-with-json-apis)
6. [Error Handling and Retries](#error-handling-and-retries)
7. [Authentication](#authentication)
8. [Best Practices](#best-practices)

---

## HTTP Fundamentals

Before diving into libraries, understand what HTTP requests involve:

### HTTP Methods

| Method | Purpose | Idempotent | Body |
|--------|---------|------------|------|
| GET | Retrieve data | Yes | No |
| POST | Create resource | No | Yes |
| PUT | Replace resource | Yes | Yes |
| PATCH | Partial update | No | Yes |
| DELETE | Remove resource | Yes | Optional |

### HTTP Status Codes

| Range | Category | Examples |
|-------|----------|----------|
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirect | 301 Moved, 302 Found, 304 Not Modified |
| 4xx | Client Error | 400 Bad Request, 401 Unauthorized, 404 Not Found |
| 5xx | Server Error | 500 Internal Error, 502 Bad Gateway, 503 Unavailable |

### Common Headers

```
Content-Type: application/json       # Request/response body format
Accept: application/json             # Acceptable response formats
Authorization: Bearer <token>        # Authentication
User-Agent: MyApp/1.0               # Client identification
```

---

## urllib: The Standard Library

`urllib.request` is Python's built-in HTTP client. It's verbose but requires no dependencies.

### Basic GET Request

```python
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import json

# Simple GET
url = "https://api.example.com/airports/KAMA"

try:
    with urlopen(url) as response:
        # Response info
        print(f"Status: {response.status}")
        print(f"Headers: {response.headers}")
        
        # Read body
        body = response.read()  # bytes
        text = body.decode("utf-8")  # string
        data = json.loads(text)  # dict
        
except HTTPError as e:
    print(f"HTTP Error: {e.code} {e.reason}")
except URLError as e:
    print(f"URL Error: {e.reason}")
```

### GET with Headers and Parameters

```python
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json

# Build URL with query parameters
base_url = "https://api.example.com/airports"
params = {"state": "TX", "limit": 10}
url = f"{base_url}?{urlencode(params)}"

# Create request with headers
request = Request(
    url,
    headers={
        "Accept": "application/json",
        "User-Agent": "AirportClient/1.0",
    }
)

with urlopen(request) as response:
    data = json.loads(response.read().decode("utf-8"))
```

### POST Request

```python
from urllib.request import urlopen, Request
import json

url = "https://api.example.com/airports"
payload = {
    "stationid": "KAMA",
    "name": "Amarillo International Airport",
}

# Encode payload as JSON bytes
data = json.dumps(payload).encode("utf-8")

request = Request(
    url,
    data=data,  # Adding data makes it a POST
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
    method="POST",
)

with urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))
```

### PUT, PATCH, DELETE

```python
from urllib.request import urlopen, Request
import json

# PUT (replace)
request = Request(
    "https://api.example.com/airports/KAMA",
    data=json.dumps({"name": "New Name"}).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="PUT",
)

# PATCH (partial update)
request = Request(
    "https://api.example.com/airports/KAMA",
    data=json.dumps({"name": "New Name"}).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="PATCH",
)

# DELETE
request = Request(
    "https://api.example.com/airports/KAMA",
    method="DELETE",
)
```

### Timeout

```python
from urllib.request import urlopen

# Set timeout (seconds)
try:
    with urlopen(url, timeout=10) as response:
        data = response.read()
except TimeoutError:
    print("Request timed out")
```

### urllib Summary

**Pros:**
- No dependencies (stdlib)
- Full control over request construction

**Cons:**
- Verbose and clunky API
- Manual JSON encoding/decoding
- No session/cookie management
- No connection pooling

---

## requests: The Ergonomic Standard

`requests` is the de facto standard for HTTP in Python. It provides an elegant, human-friendly API.

```bash
uv add requests
```

### Basic GET Request

```python
import requests

response = requests.get("https://api.example.com/airports/KAMA")

print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"JSON: {response.json()}")  # Auto-decode JSON!
```

### GET with Parameters and Headers

```python
import requests

response = requests.get(
    "https://api.example.com/airports",
    params={"state": "TX", "limit": 10},  # Auto-encoded to query string
    headers={
        "Accept": "application/json",
        "User-Agent": "AirportClient/1.0",
    },
    timeout=10,  # Always set a timeout!
)

if response.ok:  # Status 2xx
    airports = response.json()
else:
    print(f"Error: {response.status_code}")
```

### POST Request

```python
import requests

# POST with JSON body (auto-serialized)
response = requests.post(
    "https://api.example.com/airports",
    json={  # Automatically sets Content-Type and serializes
        "stationid": "KAMA",
        "name": "Amarillo International Airport",
    },
    timeout=10,
)

# POST with form data
response = requests.post(
    "https://api.example.com/login",
    data={  # Sends as application/x-www-form-urlencoded
        "username": "user",
        "password": "pass",
    },
)
```

### PUT, PATCH, DELETE

```python
import requests

# PUT
response = requests.put(
    "https://api.example.com/airports/KAMA",
    json={"name": "Updated Name"},
    timeout=10,
)

# PATCH
response = requests.patch(
    "https://api.example.com/airports/KAMA",
    json={"name": "Updated Name"},
    timeout=10,
)

# DELETE
response = requests.delete(
    "https://api.example.com/airports/KAMA",
    timeout=10,
)
```

### Sessions (Connection Pooling, Cookies)

```python
import requests

# Session maintains cookies and connection pooling
session = requests.Session()
session.headers.update({
    "User-Agent": "AirportClient/1.0",
    "Accept": "application/json",
})

# All requests through session share settings and cookies
response = session.get("https://api.example.com/airports/KAMA")
response = session.get("https://api.example.com/airports/KLBB")

# Close when done
session.close()

# Or use as context manager
with requests.Session() as session:
    session.get("https://api.example.com/airports/KAMA")
```

### Response Object

```python
import requests

response = requests.get("https://api.example.com/airports/KAMA")

# Status
response.status_code  # 200
response.ok          # True (2xx status)
response.reason      # "OK"

# Headers
response.headers["Content-Type"]  # "application/json"

# Body
response.text        # Decoded text (auto-detects encoding)
response.content     # Raw bytes
response.json()      # Parse as JSON

# Request info
response.url         # Final URL (after redirects)
response.request     # PreparedRequest object
response.elapsed     # Time taken
```

### Raise on Error

```python
import requests

response = requests.get("https://api.example.com/airports/INVALID")

# Manually check
if not response.ok:
    print(f"Error: {response.status_code}")

# Or raise exception for 4xx/5xx
response.raise_for_status()  # Raises HTTPError
```

### requests Summary

**Pros:**
- Clean, intuitive API
- Auto JSON encoding/decoding
- Session management
- Connection pooling
- Excellent documentation

**Cons:**
- External dependency
- No async support
- Some edge cases (streaming, HTTP/2)

---

## httpx: Modern Async-Capable HTTP

`httpx` is a modern HTTP client with async support, HTTP/2, and a requests-compatible API.

```bash
uv add httpx
```

### Synchronous Usage (requests-compatible)

```python
import httpx

# Almost identical to requests!
response = httpx.get(
    "https://api.example.com/airports/KAMA",
    timeout=10,
)

print(response.status_code)
print(response.json())
```

### All HTTP Methods

```python
import httpx

# GET with params
response = httpx.get(
    "https://api.example.com/airports",
    params={"state": "TX"},
    timeout=10,
)

# POST with JSON
response = httpx.post(
    "https://api.example.com/airports",
    json={"stationid": "KAMA", "name": "Amarillo"},
    timeout=10,
)

# PUT, PATCH, DELETE
response = httpx.put(url, json=data, timeout=10)
response = httpx.patch(url, json=data, timeout=10)
response = httpx.delete(url, timeout=10)
```

### Client (Sessions)

```python
import httpx

# Synchronous client
with httpx.Client(
    base_url="https://api.example.com",
    headers={"User-Agent": "AirportClient/1.0"},
    timeout=10,
) as client:
    response = client.get("/airports/KAMA")
    response = client.get("/airports/KLBB")
```

### Async Usage

The killer feature of httpx is native async support.

```python
import httpx
import asyncio

async def fetch_airport(client: httpx.AsyncClient, stationid: str) -> dict:
    """Fetch a single airport."""
    response = await client.get(f"/airports/{stationid}")
    response.raise_for_status()
    return response.json()

async def fetch_multiple_airports(stationids: list[str]) -> list[dict]:
    """Fetch multiple airports concurrently."""
    async with httpx.AsyncClient(
        base_url="https://api.example.com",
        timeout=10,
    ) as client:
        # Concurrent requests!
        tasks = [fetch_airport(client, sid) for sid in stationids]
        return await asyncio.gather(*tasks)

# Run async code
airports = asyncio.run(fetch_multiple_airports(["KAMA", "KLBB", "KMAF"]))
```

### Async with Rate Limiting

```python
import httpx
import asyncio

async def fetch_with_semaphore(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    url: str,
) -> dict:
    """Fetch with concurrency limit."""
    async with semaphore:
        response = await client.get(url)
        return response.json()

async def fetch_many_limited(urls: list[str], max_concurrent: int = 5) -> list[dict]:
    """Fetch many URLs with limited concurrency."""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [fetch_with_semaphore(client, semaphore, url) for url in urls]
        return await asyncio.gather(*tasks)
```

### Timeout Configuration

```python
import httpx

# Simple timeout (all operations)
response = httpx.get(url, timeout=10)

# Detailed timeout configuration
timeout = httpx.Timeout(
    connect=5.0,    # Connection timeout
    read=10.0,      # Read timeout
    write=10.0,     # Write timeout
    pool=5.0,       # Pool timeout
)
response = httpx.get(url, timeout=timeout)

# No timeout (not recommended!)
response = httpx.get(url, timeout=None)
```

### HTTP/2 Support

```python
import httpx

# Enable HTTP/2
with httpx.Client(http2=True) as client:
    response = client.get("https://api.example.com/airports")
    print(response.http_version)  # "HTTP/2"
```

### httpx Summary

**Pros:**
- Async support
- HTTP/2 support
- requests-compatible API
- Better timeout handling
- Type hints throughout

**Cons:**
- External dependency
- Slightly newer (less battle-tested than requests)

---

## Working with JSON APIs

### Fetching and Parsing JSON

```python
import httpx
from dataclasses import dataclass

@dataclass
class Airport:
    stationid: str
    name: str
    city: str
    state: str
    
    @classmethod
    def from_dict(cls, data: dict) -> "Airport":
        return cls(
            stationid=data["stationid"],
            name=data["name"],
            city=data.get("city", ""),
            state=data.get("state", ""),
        )

def fetch_airport(stationid: str) -> Airport:
    """Fetch airport and convert to domain object."""
    response = httpx.get(
        f"https://api.example.com/airports/{stationid}",
        timeout=10,
    )
    response.raise_for_status()
    return Airport.from_dict(response.json())
```

### Handling Pagination

```python
import httpx
from typing import Iterator

def fetch_all_airports(state: str) -> Iterator[dict]:
    """Fetch all airports with pagination."""
    with httpx.Client(
        base_url="https://api.example.com",
        timeout=10,
    ) as client:
        page = 1
        while True:
            response = client.get(
                "/airports",
                params={"state": state, "page": page, "per_page": 100},
            )
            response.raise_for_status()
            data = response.json()
            
            if not data["airports"]:
                break
                
            yield from data["airports"]
            
            if page >= data["total_pages"]:
                break
            page += 1
```

### Uploading Files

```python
import httpx
from pathlib import Path

# Upload single file
with open("airport_data.csv", "rb") as f:
    response = httpx.post(
        "https://api.example.com/upload",
        files={"file": f},
        timeout=30,
    )

# Upload with filename
response = httpx.post(
    "https://api.example.com/upload",
    files={"file": ("airports.csv", open("data.csv", "rb"), "text/csv")},
)

# Upload multiple files
response = httpx.post(
    "https://api.example.com/upload",
    files=[
        ("files", ("file1.csv", open("file1.csv", "rb"))),
        ("files", ("file2.csv", open("file2.csv", "rb"))),
    ],
)
```

---

## Error Handling and Retries

### Basic Error Handling

```python
import httpx

def fetch_airport(stationid: str) -> dict | None:
    """Fetch airport with error handling."""
    try:
        response = httpx.get(
            f"https://api.example.com/airports/{stationid}",
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
        
    except httpx.TimeoutException:
        print(f"Request timed out for {stationid}")
        return None
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            print(f"Airport {stationid} not found")
        else:
            print(f"HTTP error: {e.response.status_code}")
        return None
        
    except httpx.RequestError as e:
        print(f"Request failed: {e}")
        return None
```

### Retry with Exponential Backoff

```python
import httpx
import time
from typing import TypeVar

T = TypeVar("T")

def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> httpx.Response:
    """Fetch with exponential backoff retry."""
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            response = httpx.get(url, timeout=10)
            
            # Retry on 5xx errors
            if response.status_code >= 500:
                raise httpx.HTTPStatusError(
                    f"Server error: {response.status_code}",
                    request=response.request,
                    response=response,
                )
            
            return response
            
        except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
            last_exception = e
            
            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)  # Exponential backoff
                print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
                time.sleep(delay)
    
    raise last_exception
```

### Async Retry

```python
import httpx
import asyncio

async def fetch_with_retry_async(
    client: httpx.AsyncClient,
    url: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> httpx.Response:
    """Async fetch with exponential backoff retry."""
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response
            
        except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
            last_exception = e
            
            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
    
    raise last_exception
```

---

## Authentication

### API Key in Header

```python
import httpx

response = httpx.get(
    "https://api.example.com/airports",
    headers={"X-API-Key": "your-api-key"},
    timeout=10,
)

# Or with a client
with httpx.Client(
    headers={"X-API-Key": "your-api-key"},
) as client:
    response = client.get("https://api.example.com/airports")
```

### API Key in Query Parameter

```python
import httpx

response = httpx.get(
    "https://api.example.com/airports",
    params={"api_key": "your-api-key"},
    timeout=10,
)
```

### Basic Authentication

```python
import httpx

# Using auth parameter
response = httpx.get(
    "https://api.example.com/airports",
    auth=("username", "password"),
    timeout=10,
)

# With client
with httpx.Client(auth=("username", "password")) as client:
    response = client.get("https://api.example.com/airports")
```

### Bearer Token (OAuth)

```python
import httpx

token = "your-bearer-token"

response = httpx.get(
    "https://api.example.com/airports",
    headers={"Authorization": f"Bearer {token}"},
    timeout=10,
)

# With client
with httpx.Client(
    headers={"Authorization": f"Bearer {token}"},
) as client:
    response = client.get("https://api.example.com/airports")
```

### Custom Authentication Class

```python
import httpx
import time
import hashlib

class HMACAuth(httpx.Auth):
    """Custom HMAC authentication."""
    
    def __init__(self, api_key: str, secret: str):
        self.api_key = api_key
        self.secret = secret
    
    def auth_flow(self, request):
        timestamp = str(int(time.time()))
        signature = hashlib.sha256(
            f"{timestamp}{self.secret}".encode()
        ).hexdigest()
        
        request.headers["X-API-Key"] = self.api_key
        request.headers["X-Timestamp"] = timestamp
        request.headers["X-Signature"] = signature
        
        yield request

# Use custom auth
with httpx.Client(auth=HMACAuth("key", "secret")) as client:
    response = client.get("https://api.example.com/airports")
```

---

## Best Practices

### 1. Always Set Timeouts

```python
# BAD - can hang forever
response = httpx.get(url)

# GOOD - always set a timeout
response = httpx.get(url, timeout=10)
```

### 2. Use Sessions/Clients for Multiple Requests

```python
# BAD - new connection for each request
for stationid in stationids:
    response = httpx.get(f"{base_url}/airports/{stationid}")

# GOOD - reuse connection
with httpx.Client(base_url=base_url) as client:
    for stationid in stationids:
        response = client.get(f"/airports/{stationid}")
```

### 3. Handle Errors Gracefully

```python
# BAD - crashes on error
response = httpx.get(url)
data = response.json()

# GOOD - handle errors
try:
    response = httpx.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except httpx.HTTPStatusError as e:
    logger.error(f"HTTP error: {e.response.status_code}")
    raise
except httpx.RequestError as e:
    logger.error(f"Request failed: {e}")
    raise
```

### 4. Don't Hardcode URLs

```python
# BAD
response = httpx.get("https://api.example.com/v1/airports/KAMA")

# GOOD
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com/v1")

with httpx.Client(base_url=API_BASE_URL) as client:
    response = client.get("/airports/KAMA")
```

### 5. Use Environment Variables for Secrets

```python
import os

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")

with httpx.Client(
    headers={"X-API-Key": API_KEY},
) as client:
    response = client.get(url)
```

### 6. Log Requests for Debugging

```python
import httpx
import logging

logging.basicConfig(level=logging.DEBUG)

# httpx logs requests at DEBUG level
response = httpx.get(url)
```

### 7. Consider Rate Limits

```python
import time

def fetch_with_rate_limit(urls: list[str], requests_per_second: float = 2):
    """Fetch URLs respecting rate limits."""
    delay = 1.0 / requests_per_second
    
    with httpx.Client() as client:
        for url in urls:
            response = client.get(url)
            yield response
            time.sleep(delay)
```

---

## Library Comparison

| Feature | urllib | requests | httpx |
|---------|--------|----------|-------|
| Stdlib | ✓ | | |
| Clean API | | ✓ | ✓ |
| Auto JSON | | ✓ | ✓ |
| Sessions | | ✓ | ✓ |
| Async | | | ✓ |
| HTTP/2 | | | ✓ |
| Type hints | | | ✓ |
| Connection pooling | | ✓ | ✓ |

**Recommendations:**
- **urllib**: Use only when you can't add dependencies
- **requests**: Great for synchronous code, huge ecosystem
- **httpx**: Best for new projects, especially with async needs

---

## Further Reading

- [urllib.request documentation](https://docs.python.org/3/library/urllib.request.html)
- [requests documentation](https://requests.readthedocs.io/)
- [httpx documentation](https://www.python-httpx.org/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [REST API Tutorial](https://restfulapi.net/)
