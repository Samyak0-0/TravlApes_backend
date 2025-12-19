from datetime import datetime
from typing import Union

import bcrypt
from fastapi import FastAPI

from src.routes import dummyroute
from src.routes import destinationsRoute

from .db import destinations, users
from .models import DestinationCreate, UserCreate

app = FastAPI(title="Travlapes Backend", version="1.0.0")
app.include_router(dummyroute.router)
app.include_router(destinationsRoute.router)


@app.post("/users")
def create_user(user: UserCreate):
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    users.insert_one(
        {
            "username": user.username,
            "email": user.email,
            "password_hash": hashed_pw,
            "created_at": datetime.utcnow(),
        }
    )

    return {"message": "User created"}


# @app.post("/destinations")
# def create_destination(dest: DestinationCreate):
#     destinations.insert_one({**dest.dict(), "created_at": datetime.utcnow()})

#     return {"message": "Destination added"}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
