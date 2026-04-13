"""
HTTP and Web APIs Example

This module demonstrates three approaches to HTTP in Python:
1. urllib (stdlib) - verbose but no dependencies
2. requests - the ergonomic standard
3. httpx - modern with async support

Since we can't make real network requests in this demo, we use
a mock server pattern to show the API usage patterns.

Run with: python example.py
"""

import json
import threading
import time
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Optional imports - demo works without them
try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import httpx

    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False


# =============================================================================
# DOMAIN MODEL
# =============================================================================


@dataclass
class Airport:
    """Airport domain object."""

    stationid: str
    name: str
    city: str
    state: str
    latitude: float | None = None
    longitude: float | None = None

    def to_dict(self) -> dict:
        return {
            "stationid": self.stationid,
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Airport":
        return cls(
            stationid=data["stationid"],
            name=data["name"],
            city=data.get("city", ""),
            state=data.get("state", ""),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
        )


# =============================================================================
# MOCK API SERVER
# =============================================================================


# Sample data
MOCK_AIRPORTS = {
    "KAMA": Airport(
        "KAMA",
        "Rick Husband Amarillo International",
        "Amarillo",
        "TX",
        35.2194,
        -101.7059,
    ),
    "KLBB": Airport(
        "KLBB",
        "Lubbock Preston Smith International",
        "Lubbock",
        "TX",
        33.6636,
        -101.8228,
    ),
    "KMAF": Airport(
        "KMAF",
        "Midland International Air and Space Port",
        "Midland",
        "TX",
        31.9425,
        -102.2019,
    ),
    "KDFW": Airport(
        "KDFW",
        "Dallas/Fort Worth International",
        "Dallas",
        "TX",
        32.8998,
        -97.0403,
    ),
}


class MockAPIHandler(BaseHTTPRequestHandler):
    """Simple mock API server for demonstration."""

    def log_message(self, format, *args):
        """Suppress logging."""
        pass

    def do_GET(self):
        """Handle GET requests."""
        if self.path.startswith("/airports/"):
            stationid = self.path.split("/")[-1].upper()
            if stationid in MOCK_AIRPORTS:
                self._send_json(200, MOCK_AIRPORTS[stationid].to_dict())
            else:
                self._send_json(404, {"error": "Airport not found"})
        elif self.path.startswith("/airports"):
            # Return all airports
            airports = [a.to_dict() for a in MOCK_AIRPORTS.values()]
            self._send_json(200, {"airports": airports})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body.decode("utf-8"))
            airport = Airport.from_dict(data)
            MOCK_AIRPORTS[airport.stationid] = airport
            self._send_json(201, airport.to_dict())
        except (json.JSONDecodeError, KeyError) as e:
            self._send_json(400, {"error": str(e)})

    def do_PUT(self):
        """Handle PUT requests."""
        self.do_POST()  # Simplified for demo

    def do_DELETE(self):
        """Handle DELETE requests."""
        if self.path.startswith("/airports/"):
            stationid = self.path.split("/")[-1].upper()
            if stationid in MOCK_AIRPORTS:
                del MOCK_AIRPORTS[stationid]
                self._send_json(204, None)
            else:
                self._send_json(404, {"error": "Airport not found"})
        else:
            self._send_json(404, {"error": "Not found"})

    def _send_json(self, status: int, data: dict | None):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if data is not None:
            self.wfile.write(json.dumps(data).encode("utf-8"))


def start_mock_server(port: int = 8765) -> HTTPServer:
    """Start mock server in background thread."""
    server = HTTPServer(("localhost", port), MockAPIHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    time.sleep(0.1)  # Give server time to start
    return server


# =============================================================================
# URLLIB EXAMPLES
# =============================================================================


def urllib_get_example(base_url: str) -> None:
    """Demonstrate GET request with urllib."""
    print("\n  GET /airports/KAMA")

    url = f"{base_url}/airports/KAMA"
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "AirportClient/1.0",
        },
    )

    try:
        with urlopen(request, timeout=10) as response:
            print(f"    Status: {response.status}")
            body = response.read().decode("utf-8")
            data = json.loads(body)
            print(f"    Response: {data['stationid']} - {data['name']}")
    except HTTPError as e:
        print(f"    HTTP Error: {e.code}")
    except URLError as e:
        print(f"    URL Error: {e.reason}")


def urllib_get_with_params(base_url: str) -> None:
    """Demonstrate GET with query parameters."""
    print("\n  GET /airports?state=TX")

    params = {"state": "TX", "limit": 10}
    url = f"{base_url}/airports?{urlencode(params)}"

    with urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))
        print(f"    Found {len(data['airports'])} airports")


def urllib_post_example(base_url: str) -> None:
    """Demonstrate POST request with urllib."""
    print("\n  POST /airports (create KSAT)")

    payload = {
        "stationid": "KSAT",
        "name": "San Antonio International",
        "city": "San Antonio",
        "state": "TX",
    }

    request = Request(
        f"{base_url}/airports",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=10) as response:
        print(f"    Status: {response.status}")
        data = json.loads(response.read().decode("utf-8"))
        print(f"    Created: {data['stationid']}")


def urllib_delete_example(base_url: str) -> None:
    """Demonstrate DELETE request with urllib."""
    print("\n  DELETE /airports/KSAT")

    request = Request(
        f"{base_url}/airports/KSAT",
        method="DELETE",
    )

    with urlopen(request, timeout=10) as response:
        print(f"    Status: {response.status}")


# =============================================================================
# REQUESTS EXAMPLES
# =============================================================================


def requests_get_example(base_url: str) -> None:
    """Demonstrate GET request with requests."""
    print("\n  GET /airports/KAMA")

    response = requests.get(
        f"{base_url}/airports/KAMA",
        headers={"Accept": "application/json"},
        timeout=10,
    )

    print(f"    Status: {response.status_code}")
    if response.ok:
        data = response.json()  # Auto JSON decode!
        print(f"    Response: {data['stationid']} - {data['name']}")


def requests_get_with_params(base_url: str) -> None:
    """Demonstrate GET with query parameters."""
    print("\n  GET /airports?state=TX")

    response = requests.get(
        f"{base_url}/airports",
        params={"state": "TX", "limit": 10},  # Auto URL encoding
        timeout=10,
    )

    data = response.json()
    print(f"    Found {len(data['airports'])} airports")


def requests_post_example(base_url: str) -> None:
    """Demonstrate POST request with requests."""
    print("\n  POST /airports (create KHOU)")

    response = requests.post(
        f"{base_url}/airports",
        json={  # Auto JSON encode + Content-Type header
            "stationid": "KHOU",
            "name": "William P. Hobby Airport",
            "city": "Houston",
            "state": "TX",
        },
        timeout=10,
    )

    print(f"    Status: {response.status_code}")
    if response.ok:
        data = response.json()
        print(f"    Created: {data['stationid']}")


def requests_session_example(base_url: str) -> None:
    """Demonstrate session usage."""
    print("\n  Session example (multiple requests)")

    with requests.Session() as session:
        session.headers.update({"User-Agent": "AirportClient/1.0"})

        # Multiple requests share connection and headers
        for stationid in ["KAMA", "KLBB", "KMAF"]:
            response = session.get(f"{base_url}/airports/{stationid}", timeout=10)
            data = response.json()
            print(f"    {data['stationid']}: {data['city']}")


def requests_error_handling(base_url: str) -> None:
    """Demonstrate error handling."""
    print("\n  Error handling (404 example)")

    response = requests.get(f"{base_url}/airports/INVALID", timeout=10)

    if not response.ok:
        print(f"    Status: {response.status_code}")
        print(f"    Response: {response.json()}")


# =============================================================================
# HTTPX EXAMPLES
# =============================================================================


def httpx_get_example(base_url: str) -> None:
    """Demonstrate GET request with httpx."""
    print("\n  GET /airports/KAMA")

    response = httpx.get(
        f"{base_url}/airports/KAMA",
        timeout=10,
    )

    print(f"    Status: {response.status_code}")
    data = response.json()
    print(f"    Response: {data['stationid']} - {data['name']}")


def httpx_client_example(base_url: str) -> None:
    """Demonstrate client usage."""
    print("\n  Client example (with base_url)")

    with httpx.Client(
        base_url=base_url,
        headers={"User-Agent": "AirportClient/1.0"},
        timeout=10,
    ) as client:
        # Requests use relative URLs
        for stationid in ["KAMA", "KLBB", "KMAF"]:
            response = client.get(f"/airports/{stationid}")
            data = response.json()
            print(f"    {data['stationid']}: {data['city']}")


def httpx_post_example(base_url: str) -> None:
    """Demonstrate POST request with httpx."""
    print("\n  POST /airports (create KIAH)")

    response = httpx.post(
        f"{base_url}/airports",
        json={
            "stationid": "KIAH",
            "name": "George Bush Intercontinental",
            "city": "Houston",
            "state": "TX",
        },
        timeout=10,
    )

    print(f"    Status: {response.status_code}")
    data = response.json()
    print(f"    Created: {data['stationid']}")


def httpx_error_handling(base_url: str) -> None:
    """Demonstrate error handling with raise_for_status."""
    print("\n  Error handling with raise_for_status")

    try:
        response = httpx.get(f"{base_url}/airports/INVALID", timeout=10)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"    HTTP Error: {e.response.status_code}")
        print(f"    Response: {e.response.json()}")


# =============================================================================
# ASYNC HTTPX EXAMPLE
# =============================================================================


async def httpx_async_example(base_url: str) -> None:
    """Demonstrate async requests with httpx."""
    import asyncio

    print("\n  Async example (concurrent requests)")

    async def fetch_airport(client: httpx.AsyncClient, stationid: str) -> dict:
        response = await client.get(f"/airports/{stationid}")
        return response.json()

    async with httpx.AsyncClient(base_url=base_url, timeout=10) as client:
        # Concurrent requests
        tasks = [fetch_airport(client, sid) for sid in ["KAMA", "KLBB", "KMAF", "KDFW"]]
        results = await asyncio.gather(*tasks)

        for data in results:
            print(f"    {data['stationid']}: {data['city']}")


# =============================================================================
# COMPARISON: SAME REQUEST WITH ALL THREE LIBRARIES
# =============================================================================


def compare_libraries(base_url: str) -> None:
    """Show the same request with all three libraries."""

    print("\n  Fetching KAMA with each library:")

    # urllib
    print("\n  urllib:")
    code = """    request = Request(f"{base_url}/airports/KAMA")
    with urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))"""
    print(code)

    request = Request(f"{base_url}/airports/KAMA")
    with urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))
        print(f"    Result: {data['stationid']}")

    # requests
    if REQUESTS_AVAILABLE:
        print("\n  requests:")
        code = """    response = requests.get(f"{base_url}/airports/KAMA")
    data = response.json()"""
        print(code)

        response = requests.get(f"{base_url}/airports/KAMA", timeout=10)
        data = response.json()
        print(f"    Result: {data['stationid']}")

    # httpx
    if HTTPX_AVAILABLE:
        print("\n  httpx:")
        code = """    response = httpx.get(f"{base_url}/airports/KAMA")
    data = response.json()"""
        print(code)

        response = httpx.get(f"{base_url}/airports/KAMA", timeout=10)
        data = response.json()
        print(f"    Result: {data['stationid']}")


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================


def main() -> None:  # noqa: PLR0915
    """Demonstrate HTTP client libraries."""

    print("=" * 70)
    print("HTTP AND WEB APIS DEMONSTRATION")
    print("=" * 70)

    # Start mock server
    port = 8765
    server = start_mock_server(port)
    base_url = f"http://localhost:{port}"

    print(f"\nMock API server running at {base_url}")

    try:
        # ---------------------------------------------------------------------
        # 1. URLLIB (STDLIB)
        # ---------------------------------------------------------------------

        print("\n" + "=" * 70)
        print("1. URLLIB (Standard Library)")
        print("=" * 70)

        urllib_get_example(base_url)
        urllib_get_with_params(base_url)
        urllib_post_example(base_url)
        urllib_delete_example(base_url)

        # ---------------------------------------------------------------------
        # 2. REQUESTS
        # ---------------------------------------------------------------------

        print("\n" + "=" * 70)
        print("2. REQUESTS")
        print("=" * 70)

        if REQUESTS_AVAILABLE:
            requests_get_example(base_url)
            requests_get_with_params(base_url)
            requests_post_example(base_url)
            requests_session_example(base_url)
            requests_error_handling(base_url)
        else:
            print("\n  requests not installed. Run: uv add requests")

        # ---------------------------------------------------------------------
        # 3. HTTPX
        # ---------------------------------------------------------------------

        print("\n" + "=" * 70)
        print("3. HTTPX")
        print("=" * 70)

        if HTTPX_AVAILABLE:
            httpx_get_example(base_url)
            httpx_client_example(base_url)
            httpx_post_example(base_url)
            httpx_error_handling(base_url)

            # Async example
            import asyncio

            print("\n  --- Async Support ---")
            asyncio.run(httpx_async_example(base_url))
        else:
            print("\n  httpx not installed. Run: uv add httpx")

        # ---------------------------------------------------------------------
        # 4. COMPARISON
        # ---------------------------------------------------------------------

        print("\n" + "=" * 70)
        print("4. LIBRARY COMPARISON")
        print("=" * 70)

        compare_libraries(base_url)

        # ---------------------------------------------------------------------
        # 5. SUMMARY
        # ---------------------------------------------------------------------

        print("\n" + "=" * 70)
        print("5. SUMMARY")
        print("=" * 70)

        print("""
  | Feature           | urllib | requests | httpx |
  |-------------------|--------|----------|-------|
  | Stdlib            |   ✓    |          |       |
  | Clean API         |        |    ✓     |   ✓   |
  | Auto JSON         |        |    ✓     |   ✓   |
  | Sessions/Clients  |        |    ✓     |   ✓   |
  | Async support     |        |          |   ✓   |
  | HTTP/2 support    |        |          |   ✓   |

  Recommendations:
  - urllib:   When you can't add dependencies
  - requests: Great for synchronous code, huge ecosystem
  - httpx:    Best for new projects, especially with async
        """)

    finally:
        server.shutdown()

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
