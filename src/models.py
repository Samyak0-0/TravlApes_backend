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




MOOD_TO_CATEGORY = {
    Mood.food: [
        Category.restaurant,
    ],

    Mood.entertainment: [
        Category.other,
        Category.park,
    ],

    Mood.cultural: [
        Category.heritage,
        Category.temple,
    ],

    Mood.peaceful: [
        Category.park,
        Category.lakes,
        Category.temple,
        Category.rivers,
        Category.peaks,
    ],

    Mood.adventurous: [
        Category.peaks,
        Category.waterfalls,
        Category.rivers,
    ],

    Mood.nature: [
        Category.park,
        Category.lakes,
        Category.rivers,
        Category.waterfalls,
        Category.picnic_site,
    ],
}

MOOD_COMPLEMENTARY = {
    Mood.food: [
        Mood.entertainment,
        Mood.cultural,
        Mood.peaceful,
    ],

    Mood.entertainment: [
        Mood.food,
        Mood.adventurous,
    ],

    Mood.cultural: [
        Mood.food,
        Mood.peaceful,
        Mood.nature,
    ],

    Mood.peaceful: [
        Mood.nature,
        Mood.cultural,
        Mood.food,
    ],

    Mood.adventurous: [
        Mood.entertainment,
        Mood.nature,
    ],

    Mood.nature: [
        Mood.peaceful,
        Mood.adventurous,
        Mood.cultural,
    ],
}

