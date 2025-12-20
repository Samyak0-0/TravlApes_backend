from datetime import date as date_cls
from datetime import datetime

import requests

from .models import Season, Weather


def get_season(date_str: str) -> Season:
    month = datetime.strptime(date_str, "%Y-%m-%d").month

    if month in (3, 4, 5):
        return Season.spring
    elif month in (6, 7, 8):
        return Season.summer
    elif month in (9, 10, 11):
        return Season.autumn
    else:
        return Season.winter


def get_weather_for_date(
    latitude: float,
    longitude: float,
    date_str: str,
    timezone: str = "Asia/Kathmandu",
) -> Weather:
    query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    today = date_cls.today()

    # Choose correct endpoint
    if query_date <= today:
        base_url = "https://archive-api.open-meteo.com/v1/archive"
    else:
        base_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": date_str,
        "end_date": date_str,
        "daily": "precipitation_sum,cloudcover_mean",
        "timezone": timezone,
    }

    resp = requests.get(base_url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    daily = data.get("daily")
    if not daily:
        raise RuntimeError(f"No daily weather data returned: {data}")

    precipitation = daily["precipitation_sum"][0]
    cloudcover = daily["cloudcover_mean"][0]

    if precipitation > 0:
        return Weather.rainy
    elif cloudcover > 60:
        return Weather.cloudy
    else:
        return Weather.sunny
