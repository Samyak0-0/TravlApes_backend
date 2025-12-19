from fastapi import APIRouter, HTTPException

from ..db import destinations
from ..models import DestinationCreate, DestinationFilter

router = APIRouter(prefix="/destinations", tags=["destinations"])


@router.get("/")
def list_all_destinations():
    # Find all destinations and convert cursor to list
    all_destinations = list(destinations.find())

    # Convert MongoDB _id to string for JSON serialization
    for dest in all_destinations:
        dest["_id"] = str(dest["_id"])

    return {"status": "ok", "data": all_destinations, "count": len(all_destinations)}


@router.post("/")
def create_destination(dest: DestinationCreate):
    # Check if destination with same id already exists
    if destinations.find_one({"id": dest.id}):
        raise HTTPException(
            status_code=400, detail="Destination with this ID already exists"
        )

    # Insert into MongoDB
    destinations.insert_one(
        {
            **dest.dict(),
        }
    )

    return {"message": "Destination added successfully"}


@router.post("/search")
def search_destinations(filters: DestinationFilter):
    query = {}

    if filters.location:
        query["location"] = filters.location

    if filters.category:
        query["category"] = {"$in": filters.category}

    if filters.moods:
        query["compatable_moods"] = {"$in": filters.moods}

    results = list(destinations.find(query))
    for r in results:
        r["_id"] = str(r["_id"])
    return results
