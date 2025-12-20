#osrmRoute.py

from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(
    prefix="/route",
    tags=["Routing"]
)

OSRM_SERVICES = {
    "car": "http://localhost:5001",
    "bike": "http://localhost:5002",
    "foot": "http://localhost:5003",
}

OSRM_PROFILE_MAP = {
    "car": "driving",
    "bike": "cycling",
    "foot": "foot",
}

@router.get("/")
async def get_route(
    profile: str,
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
):
    if profile not in OSRM_SERVICES:
        raise HTTPException(status_code=400, detail="Invalid profile")

    osrm_profile = OSRM_PROFILE_MAP[profile]

    url = (
        f"{OSRM_SERVICES[profile]}/route/v1/{osrm_profile}/"
        f"{start_lon},{start_lat};{end_lon},{end_lat}"
        "?overview=full&geometries=geojson"
    )

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=response.text
        )

    data = response.json()

    if not data.get("routes"):
        raise HTTPException(
            status_code=404,
            detail="No route found"
        )

    route = data["routes"][0]

    return {
        "distance_m": route["distance"],
        "duration_s": route["duration"],
        "coordinates": route["geometry"]["coordinates"],  # 👈 IMPORTANT
    }
