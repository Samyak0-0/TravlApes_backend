from typing import List

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class DestinationCreate(BaseModel):
    id: int
    place: str | None = None
    location: str | None = None
    category: str
    name: str
    hours: str
    price: str
    description: str
    latitude: float | None = None
    longitude: float | None = None
