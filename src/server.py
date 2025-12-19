from typing import Union

from fastapi import FastAPI

from src.routes import dummyroute

app = FastAPI(title="Travlapes Backend", version="1.0.0")
app.include_router(dummyroute.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
