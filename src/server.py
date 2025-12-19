from datetime import datetime
from typing import Union

import bcrypt
from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
# from hashing import Hash
from src.routes import dummyroute
from src.routes import destinationsRoute
from .jwttoken import create_access_token

from .db import destinations, users
from .models import DestinationCreate, UserCreate

app = FastAPI(title="Travlapes Backend", version="1.0.0")
# NOTE: For development you can allow all origins. In production, replace
# "*" with an explicit list of allowed origins, e.g. ["http://192.168.1.10:3000"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dummyroute.router)
app.include_router(destinationsRoute.router)


# @app.post("/register")
# def create_user(user: UserCreate):
#     hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

#     users.insert_one(
#         {
#             "username": user.username,
#             "email": user.email,
#             "password_hash": hashed_pw,
#             "created_at": datetime.utcnow(),
#         }
#     )

#     return {"message": "User created"}

# app.post('/register')
# def create_user(request: UserCreate):
#     hashed_pass = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt())
#     user_object = dict(request)
#     user_object["password"] = hashed_pass
#     user_id = users.insert(user_object)
#     #print(user)
#     return {"res": f"{user_id} created"}   
@app.post('/register')
def create_user(request: UserCreate):
    hashed_pass = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
    user_object = dict(request)
    user_object["password"] = hashed_pass.decode('utf-8')  # Crucial fix!
    users.insert_one(user_object)
    # print(user_id)
    return {"msg": "User created successfully"}

@app.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
    user = users.find_one({"username": request.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No user found with username {request.username}'
        )
    
    if not bcrypt.checkpw(request.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Wrong username or password'
        )

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


# @app.post('/login')
# def login(request:OAuth2PasswordRequestForm = Depends()):
# 	user = UserCreate.find_one({"username":request.username})
# 	if not user:
# 		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
# 	if not bcrypt.checkpw(request.password.encode('utf-8'), user["password"].encode('utf-8')):
# 		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
# 	access_token = create_access_token(data={"sub": user["username"] })
# 	return {"access_token": access_token, "token_type": "bearer"}

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
