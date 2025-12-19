from typing import List, Optional

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

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None