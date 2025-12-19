from typing import List

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class DestinationCreate(BaseModel):
    name: str
    country: str
    difficulty: str
    avg_cost: int
    duration_days: int
    tags: List[str]
