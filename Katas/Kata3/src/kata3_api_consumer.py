import os
import json
import time
import requests
from dotenv import load_dotenv

def fetch_fred_data_with_retry(base_url, params, max_retries=6):
    """
    Fetch data from FRED API with retry logic and exponential backoff.

    Maximum of 6 retries for maximum resilience in production environment.
    
    Returns: response object or None if all retries failed
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(base_url, params=params, timeout=10)
            
            # If successful (200), return it
            if response.status_code == 200:
                return response
            
            # If it's a temporary error (5xx), retry
            if 500 <= response.status_code < 600:
                wait_time = 2 ** attempt  # 1, 2, 4, 8... seconds
                print(f"Attempt {attempt + 1} failed with {response.status_code}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                # If it's not a temporary error (like 404), don't retry
                return response
                
        except requests.exceptions.RequestException as e:
            wait_time = 2 ** attempt
            print(f"Request failed: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    # If we exhausted retries, return None
    return None

load_dotenv()
api_key = os.getenv('FRED_API_KEY')
# Define where FRED is
base_url = "https://api.stlouisfed.org/fred/series/observations"

# What data do you want?
series_id = "UNRATE"

# Package the parameters
params = {
    "series_id": series_id,
    "api_key": api_key,
    "file_type": "json"
}
# Make the request with retry logic
response = fetch_fred_data_with_retry(base_url, params)
if response and response.status_code == 200:
    data = response.json()
    observations = data['observations']
    print(f"Success! Got {len(observations)} observations")
        # Save to JSON file
    with open('../data/unrate_data.json', 'w') as f:
        json.dump(observations, f, indent=2)
    print("Data saved to data/unrate_data.json")
else:
    if response:
        print(f"Error: {response.status_code} - {response.text}")
    else:
        print("Error: Failed to fetch data after all retries exhausted")
