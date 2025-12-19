from typing import List, Optional
import json
from pydantic import BaseModel, Field, conlist
from enum import Enum

# "food", "entertainment", "culture", "peaceful", "adventurous", "nature"
# "sunny", "rainy", "cloudy"
# "summer", "winter", "autumn"

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

class Category(str, Enum):
    restaurant = "restaurant"
    accomodations = "accomodations"
    peaks = "peaks"
    lakes = "lakes"
    rivers = "rivers"
    waterfalls = "waterfalls"
    picnic_site = "picnic_site"
    heritage = "heritage"
    park = "park"
    temple = "temple"
    other = "other"

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class DestinationCreate(BaseModel):
    id: int
    location: str
    name: str
    description: str
    category: Category
    avg_price: float
    rating: float
    open_hours: str
    latitude: float
    longitude: float
    suitable_season: List[Season]
    suitable_weather: List[Weather]
    compatable_moods: List[Mood]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
