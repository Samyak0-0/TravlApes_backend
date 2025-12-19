from typing import List

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class DestinationCreate(BaseModel):
    id: int
    place: str
    location: str
    category: str
    Name: str
    hours: str 
    price: str
    descripiton: str
