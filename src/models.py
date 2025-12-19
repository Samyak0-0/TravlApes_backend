from typing import List, Optional
import json
from pydantic import BaseModel, Field, conlist
from enum import Enum

class Mood(str, Enum):
    food = "food"
    entertainment = "entertainment"
    cultural = "cultural"
    peaceful = "peaceful"
    adventurous = "adventurous"
    nature = "nature"

class Weather(str, Enum):
    sunny = "sunny"
    rainy = "rainy"
    cloudy = "cloudy"

class Season(str, Enum):
    summer = "summer"
    winter = "winter"
    autumn = "autumn"

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class DestinationCreate(BaseModel):
    id: int
    location: str
    name: str
    description: str
    avg_price: str
    rating: float
    open_hours: str
    latitude: float
    longitude: float
    suitable_season: List[Season]
    suitable_weather: List[Weather]
    compatable_moods: List[Mood]

