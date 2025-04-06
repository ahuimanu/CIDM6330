from datetime import datetime
from prophet.serialize import model_to_json, model_from_json
from django.core.cache import cache
from ninja import Router, Field, Schema
import pandas as pd
import requests


def load_model():
    with open("./apilist/utils/model.json", "r") as fin:
        return model_from_json(fin.read())


router = Router()


class CityRecommendationRequestSchema(Schema):
    travel_date: str = Field(..., description="Date of travel in YYYY-MM-DD format")
    origin_city: str = Field(..., description="Origin city name")
    destination_city: str = Field(..., description="Destination city name")


class CityRecommendationResponse(Schema):
    recommendation: str = Field(
        ..., description="Travel recommendation based on temperature comparison"
    )


class CityWeatherPredictionRequest(Schema):
    city: str = Field(..., description="City name")
    date: str = Field(..., description="Date of prediction in YYYY-MM-DD format")


class CityWeatherPredictionResponse(Schema):
    predicted_temperature: float = Field(
        ..., description="Weather prediction for the specified city and date"
    )

@router.get("hello/", url_name="hello")
def hello(request):
    return {"message": "Hello, World!"}   

@router.get("/v1/", url_name="welcome")
def welcome(request):
    return {"message": "Welcome to the Travel Management API"}


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


@router.post("/city_weather_prediction/")
async def weather_prediction(request, data: CityWeatherPredictionRequest):
    try:
        city = None
        m = None
        # Extract city and date from the request data
        if data.city == "Los Angeles,CA":
            city = "LA"
            la_m = cache.get("serialized_model_la")
            if la_m is None:
                # Load the model from the file and return it.
                with open("./apilist/utils/la_model.json", "r") as fin:
                    la_m = model_from_json(fin.read())

            # generalized load
            m = la_m

        elif data.city == "New York,NY":
            city = "NY"
            nyc_m = cache.get("serialized_model_nyc")
            if nyc_m is None:
                # Load the model from the file and return it.
                with open("./apilist/utils/nyc_model.json", "r") as fin:
                    nyc_m = model_from_json(fin.read())

            # generalized load
            m = nyc_m

        # Extract input date from the request data
        input_date_str = data.date
        input_date = datetime.strptime(input_date_str, "%Y-%m-%d")

        # Create a dataframe with the input date
        future_df = pd.DataFrame({"ds": [input_date]})

        # Make predictions
        forecast = m.predict(future_df)

        # Extract the predicted temperature for the input date
        predicted_temperature = forecast.loc[0, "yhat"]

        return CityWeatherPredictionResponse(
            predicted_temperature=predicted_temperature
        )
    except FileNotFoundError:
        # Handle the case where the model file is not found
        return {"error": "Model file not found."}

    except Exception as e:
        # Handle exceptions and return an error response
        return {"error": str(e)}
