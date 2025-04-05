from django.core.cache import cache
from prophet.serialize import model_to_json, model_from_json
from celery import shared_task
import requests
import datetime

"""
This module contains the Celery task to fetch and store temperature data for cities.
Credit to: Afroza Nowshin
"""


@shared_task
def load_model(city: str):
    try:
        if city == "LA":
            # Load the model from the file and return it.
            with open("./apilist/utils/la_model.json", "r") as fin:
                la_m = model_from_json(fin.read())

            # Load the model from the file and return it.
            cache.set("serialized_model_la", la_m, timeout=None)  # infinite caching
        elif city == "NY":
            # Load the model from the file and return it.
            with open("./apilist/utils/nyc_model.json", "r") as fin:
                ny_m = model_from_json(fin.read())

            # Load the model from the file and return it.
            cache.set("serialized_model_ny", ny_m, timeout=None)

    except FileNotFoundError:
        print("Model file not found.")


@shared_task
def fetch_and_store_temperature():
    try:
        # https://raw.githubusercontent.com/ahuimanu/CIDM6330/SPRING2025/CIDM6330-Spring2025/Resources/cities.json
        response = requests.get(
            "https://raw.githubusercontent.com/ahuimanu/CIDM6330/SPRING2025/CIDM6330-Spring2025/Resources/cities.json"
        )
        response.raise_for_status()

        cities_data = response.json().get("cities", [])

        all_temperatures = []

        for city in cities_data:
            latitude = city.get("lat")
            longitude = city.get("long")

            if latitude is not None and longitude is not None:
                api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&timezone=GMT&forecast_days=7"

                weather_response = requests.get(api_url)
                weather_response.raise_for_status()

                weather_data = weather_response.json()
                hourly_data = weather_data.get("hourly", {})
                temperature_at_2pm = hourly_data.get("temperature_2m", [])

                # Cache key for each district without specifying a travel date
                cache_key = f'temperature_at_2pm_{city["name"]}'
                cache.set(cache_key, temperature_at_2pm)

                # print("checking", cache.get(cache_key))

                all_temperatures.extend(temperature_at_2pm)

        # Store all temperatures in a single cache key
        cache.set("temperature_data", all_temperatures)

    except requests.exceptions.RequestException as e:
        # Handle API request exceptions
        print(f"Error fetching weather data: {e}")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
