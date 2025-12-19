from datetime import datetime
from typing import Union

import bcrypt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from src.routes import dummyroute
from src.routes import destinationsRoute
from src.routes import osrmRoute

from src.jwttoken import create_access_token
from src.db import users
from src.models import UserCreate

# ---------------------------
# APP INIT
# ---------------------------
app = FastAPI(
    title="Travlapes Backend",
    version="1.0.0"
)

# ---------------------------
# CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# ROUTERS
# ---------------------------
app.include_router(dummyroute.router)
app.include_router(destinationsRoute.router)
app.include_router(osrmRoute.router)

# ---------------------------
# AUTH
# ---------------------------
@app.post("/register", status_code=201)
def register(user: UserCreate):
    if users.find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    hashed_pw = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    users.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed_pw,
        "created_at": datetime.utcnow()
    })

    return {"message": "User registered successfully"}


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = users.find_one({"username": form.username})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(
        form.password.encode("utf-8"),
        user["password"].encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

# ---------------------------
# HEALTH
# ---------------------------
@app.get("/")
def root():
    return {"status": "Server running"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
