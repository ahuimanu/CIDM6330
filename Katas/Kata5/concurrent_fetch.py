import json
import requests
from pathlib import Path
from typing import Tuple, List, Any
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor
import threading

# Load environment variables
dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=dotenv_path)

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

# Lock for thread-safe file writing
write_lock = threading.Lock()
RESULTS_DIR = Path(__file__).parent / "results"
LOGS_DIR = Path(__file__).parent / "logs"

def fetch_series(series_id: str, api_key: str, timeout: int) -> Tuple[str, Any]:
    """
    Fetch a single FRED series.
    
    Args:
        series_id: FRED series identifier (e.g., "CPIAUCSL")
        api_key: FRED API key
        timeout: Request timeout in seconds
    
    Returns:
        (series_id, data_or_error) where:
        - data_or_error is a list of observations on success
        - data_or_error is an error string on failure
    """
    try:
        # Build params dict - these are URL query parameters for FRED API
        params = {
            "series_id": series_id,      # Which series to fetch (e.g., "CPIAUCSL")
            "api_key": api_key,          # Your API key for authentication
            "file_type": "json"          # Request JSON format (not XML or CSV)
        }
        
        # Make GET request to FRED API endpoint
        # timeout prevents hanging if server is slow
        response = requests.get(FRED_BASE, params=params, timeout=timeout)
        
        # raise_for_status() throws an exception if HTTP status is 4xx or 5xx
        # (e.g., 404 Not Found, 401 Unauthorized, 500 Server Error)
        response.raise_for_status()
        
        # Parse the JSON response and extract the "observations" list
        # FRED API returns: {"observations": [{...}, {...}], ...}
        data = response.json()
        observations = data.get("observations", [])
        
        # Return tuple: (series_id, observations_list)
        return (series_id, observations)
        
    except requests.exceptions.Timeout:
        # Handle timeout
        error_msg = f"Timeout fetching {series_id}"
        return (series_id, error_msg)
    
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (401, 404, 500, etc.)
        error_msg = f"HTTP error for {series_id}: {e.response.status_code}"
        return (series_id, error_msg)
    
    except requests.exceptions.RequestException as e:
        # Handle other request errors (connection, etc.)
        error_msg = f"Request error for {series_id}: {str(e)}"
        return (series_id, error_msg)
    
    except json.JSONDecodeError:
        # Handle JSON parsing errors
        error_msg = f"Invalid JSON response for {series_id}"
        return (series_id, error_msg)
    
    except Exception as e:
        # Catch any other unexpected errors
        error_msg = f"Unexpected error for {series_id}: {str(e)}"
        return (series_id, error_msg)


def write_results(results: dict):
    """
    Write successful results to combined JSON and errors to log file.
    Thread-safe using Lock.
    
    Args:
        results: Dict mapping series_id -> (observations_list or error_string)
    """
    success_data = {}
    errors_list = []
    
    # Separate successes from errors
    for series_id, result in results.items():
        if isinstance(result, str):
            # Error message
            errors_list.append(f"{series_id}: {result}")
        else:
            # Successful observations
            success_data[series_id] = result
    
    # Write successful results to JSON file
    if success_data:
        with write_lock:
            output_file = RESULTS_DIR / "combined_results.json"
            with open(output_file, "w") as f:
                json.dump(success_data, f, indent=2)
            print(f"✓ Wrote {len(success_data)} successful series to {output_file}")
    
    # Write errors to log file
    if errors_list:
        with write_lock:
            log_file = LOGS_DIR / "errors.log"
            with open(log_file, "w") as f:
                f.write("\n".join(errors_list))
            print(f"✓ Wrote {len(errors_list)} errors to {log_file}")
    else:
        print("✓ No errors encountered!")


def fetch_all_concurrent(config: dict, api_key: str) -> dict:
    """
    Fetch all series concurrently using ThreadPoolExecutor.
    
    Args:
        config: Configuration dict with "series", "pool_size", "timeout"
        api_key: FRED API key
    
    Returns:
        Dict mapping series_id -> (observations or error_string)
    """
    results = {}
    
    # Create thread pool with size from config
    with ThreadPoolExecutor(max_workers=config["pool_size"]) as executor:
        # Submit all series as tasks to the executor
        futures = [
            executor.submit(fetch_series, series_id, api_key, config["timeout"])
            for series_id in config["series"]
        ]
        
        # Collect results as they complete
        for future in futures:
            series_id, result = future.result()
            results[series_id] = result
    
    return results


if __name__ == "__main__":
    # Load config
    config = json.load(open("config.json"))
    api_key = os.getenv("FRED_API_KEY")
    
    print("Fetching all series concurrently...")
    results = fetch_all_concurrent(config, api_key)
    
    print("\n" + "="*50)
    print("RESULTS:")
    print("="*50)
    for series_id, result in results.items():
        print(f"\n{series_id}:")
        if isinstance(result, str):
            print(f"  ❌ ERROR: {result}")
        else:
            print(f"  ✓ SUCCESS: {len(result)} observations")
    
    # Write results to files
    print("\n" + "="*50)
    print("WRITING TO FILES:")
    print("="*50)
    write_results(results)
