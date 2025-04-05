import requests
from django.core.cache import cache
from ninja import Router, Field, Schema
import pandas as pd
from datetime import datetime

router = Router()


class CityRecommendationRequestSchema(Schema):
    travel_date: str = Field(..., description="Date of travel in YYYY-MM-DD format")
    origin_city: str = Field(..., description="Origin city name")
    destination_city: str = Field(..., description="Destination city name")


class CityRecommendationResponse(Schema):
    recommendation: str = Field(
        ..., description="Travel recommendation based on temperature comparison"
    )


@router.post("/cities_recommendation/")
def show_cities_travel_recommendation(request, data: CityRecommendationRequestSchema):
    travel_date = data.travel_date
    origin_city = data.origin_city
    destination_city = data.destination_city

    # Retrieve temperatures for origin city
    origin_city_cache_key = f"temperature_at_2pm_{origin_city}"
    origin_city_temperature_at_2pm = cache.get(origin_city_cache_key)

    # Retrieve temperatures for destination city
    destination_city_cache_key = f"temperature_at_2pm_{destination_city}"
    destination_city_temperature_at_2pm = cache.get(destination_city_cache_key)

    # Check if temperatures are available in the cache
    if (
        origin_city_temperature_at_2pm is not None
        or destination_city_temperature_at_2pm is not None
    ):
        origin_city_average_temparature = sum(origin_city_temperature_at_2pm) / len(
            origin_city_temperature_at_2pm
        )

        destination_city_average_temparature = sum(
            destination_city_temperature_at_2pm
        ) / len(destination_city_temperature_at_2pm)

        # Compare the average temperatures
        # THE BUSINESS RULES ARE:
        # If the average temperature of the origin city is greater than the destination city
        # recommend traveling from origin to destination.
        if origin_city_average_temparature > destination_city_average_temparature:
            recommendation = f"Travel from {origin_city} ({origin_city_average_temparature}) to {destination_city} ({destination_city_average_temparature}) is recommended as {destination_city} is cooler ."
        else:
            recommendation = f"Travel from {origin_city} ({origin_city_average_temparature})  to {destination_city} ({destination_city_average_temparature}) is NOT recommended as destination is hotter."

        recommendation_result = CityRecommendationResponse(
            recommendation=recommendation
        )

        return recommendation_result
