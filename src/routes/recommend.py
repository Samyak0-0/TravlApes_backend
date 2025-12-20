from fastapi import APIRouter, HTTPException
from ..db import destinations
from ..models import DestinationCreate, RecommendationRequest, FinalizedPlacesRequest
from ..place_recommender import generate_recommendations, distribute_places_into_days

router = APIRouter(prefix="/places", tags=["Recommendation"])

@router.post("/recommend")
def get_recommendation(req: RecommendationRequest):
    location = req.location
    from_date = req.from_date
    to_date = req.to_date
    moods = req.moods
    budget = req.budget

    places = list(
        destinations.find(
            {"location": location},
            {"_id": 0}  # 👈 IMPORTANT
        )
    )

    if not places:
        raise HTTPException(
            status_code=400,
            detail="Invalid Location"
        )

    recommendations = generate_recommendations(
        places,
        from_date,
        to_date,
        moods,
        budget
    )

    return recommendations


@router.post("/finalize")
def finalize_places(req: FinalizedPlacesRequest):
  return distribute_places_into_days(
      req.primary_attractions,
      req.secondary_attractions,
      req.food_places,
      req.accomodations,
      req.from_date,
      req.to_date
  )

