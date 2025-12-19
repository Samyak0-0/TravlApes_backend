from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..db import destinations
from ..models import DestinationCreate

router = APIRouter(prefix="/destinations", tags=["destinations"])


@router.get("/")
def list_all_destinations():
    # Find all destinations and convert cursor to list
    all_destinations = list(destinations.find())
    
    # Convert MongoDB _id to string for JSON serialization
    for dest in all_destinations:
        dest["_id"] = str(dest["_id"])
    
    return {
        "status": "ok",
        "data": all_destinations,
        "count": len(all_destinations)
    }


@router.post("/")
def create_destination(dest: DestinationCreate):
    # Check if destination with same id already exists
    if destinations.find_one({"id": dest.id}):
        raise HTTPException(status_code=400, detail="Destination with this ID already exists")
    
    # Insert into MongoDB
    destinations.insert_one({**dest.dict(),})
    
    return {"message": "Destination added successfully"}
