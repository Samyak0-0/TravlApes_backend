import json
import math
from src.models import *
from datetime import datetime

# TODO: Make sure that each attraction have atleast 2/3 secondary attraction, food, accomodation

with open("kathmandu.json", "r") as f:
  data = json.load(f)

# Inputs
location = "Kathmandu"
from_date = "2025-12-20"
to_date = "2025-12-25"
moods = [ Mood.entertainment ]
budget = 10000


def haversine(lat1, lon1, lat2, lon2):
  R = 6371  # Earth radius in km

  phi1, phi2 = math.radians(lat1), math.radians(lat2)
  dphi = math.radians(lat2 - lat1)
  dlambda = math.radians(lon2 - lon1)

  a = (
      math.sin(dphi / 2) ** 2
      + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
  )

  return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def filter_within_radius(
  primary_attractions,
  other_attractions,
  radius_km=2.0
):
  filtered = []

  for score, place in other_attractions:
    lat = float(place["latitude"])
    lon = float(place["longitude"])

    for _, primary in primary_attractions:
      d = haversine(
        lat, lon,
        float(primary["latitude"]),
        float(primary["longitude"])
      )

      if d <= radius_km:
        filtered.append((score, place))
        break  # no need to check other primaries

  return filtered


def generate_recommendations(
  places_data: List[DestinationCreate],
  from_date: str,
  to_date: str,
  moods: List[Mood],
  budget: float
):
  trip_days = (datetime.fromisoformat(to_date) - datetime.fromisoformat(from_date)).days + 1

  primary_attractions = []
  secondary_attractions = []
  food_places = []
  accomodations = []

  recommended_primary_attractions = 0
  recommended_secondary_attractions = 0
  recommended_food_places = 0
  recommended_accomodations = 0

  # Collecting the primary attractions
  for place in places_data:
    score = 0

    for mood in moods:
      categories = MOOD_TO_CATEGORY[mood]

      if place["category"] not in categories:
        continue

      for comp_mood in place["compatable_moods"]:
        if mood == comp_mood:
          score += 1

    if score > 0:
      primary_attractions.append((score, place))


  # Remove primary attractions from the data
  used_values = {id(v) for _, v in primary_attractions}
  primary_attraction_removed_data = [v for v in places_data if id(v) not in used_values]


  # Collecting secondary Attraction

  for place in primary_attraction_removed_data:
    score = 0

    for mood in moods:
      complementary_moods = MOOD_COMPLEMENTARY[mood]

      for complementary_mood in complementary_moods:
        categories = MOOD_TO_CATEGORY[complementary_mood]
        if place["category"] in categories:
          for compatable_mood in place["compatable_moods"]:
            if complementary_mood == compatable_mood:
              score += 1

    if score > 0:
      secondary_attractions.append((score, place))


  # Collecting Food Places
  if Mood.food not in moods:
    for place in places_data:
      if place["category"] != Category.restaurant:
        continue

      score = 0
      for mood in moods:
        for compatable_mood in place["compatable_moods"]:
          if mood == compatable_mood:
            score += 1

      if score > 0:
        food_places.append((score, place))


  # Collecting accomodations
  for place in data:
    if place["category"] != Category.accomodations:
      continue

    score = 0
    for mood in moods:
      for compatable_mood in place["compatable_moods"]:
        if mood == compatable_mood:
          score += 1

    if score > 0:
      accomodations.append((score, place))


  # Remove the places that are too far away
  secondary_attractions = filter_within_radius(
    primary_attractions,
    secondary_attractions,
    radius_km=2.5
  )
  food_places = filter_within_radius(
    primary_attractions,
    food_places,
    radius_km=1.5
  )
  accomodations = filter_within_radius(
    primary_attractions,
    accomodations,
    radius_km=2.0
  )

  # Sort according to score + rating
  primary_attractions = sorted(
    primary_attractions,
    key=lambda x: x[0] + float(x[1].get("rating", 0)),
    reverse=True
  )
  secondary_attractions = sorted(
    secondary_attractions,
    key=lambda x: x[0] + float(x[1].get("rating", 0)),
    reverse=True
  )
  food_places = sorted(
    food_places,
    key=lambda x: x[0] + float(x[1].get("rating", 0)),
    reverse=True
  )
  accomodations = sorted(
    accomodations,
    key=lambda x: x[0] + float(x[1].get("rating", 0)),
    reverse=True
  )

  # No accomodations needed for a 1 day trip

  budget_for_accomodation = budget * 0.3

  if trip_days <= 1:
    accomodations = []
  else:
    for (score, place) in accomodations:
      if budget_for_accomodation >= place["avg_price"] * (trip_days - 1):
        budget -= place["avg_price"] * (trip_days - 1)
        recommended_accomodations += 1
        break

  # Calculating budget for foods
  budget_for_food = budget * 0.3
  for (score, place) in food_places:
    if budget_for_food >= place["avg_price"]:
      budget -= place["avg_price"]
      recommended_food_places += 1

  # Calculating budget for primary attraction
  budget_for_primary_attraction = budget * 0.3
  for (score, place) in primary_attractions:
    if budget_for_primary_attraction >= place["avg_price"]:
      budget -= place["avg_price"]
      recommended_primary_attractions += 1

  # Calculating budget for secondary attraction
  budget_for_secondary_attraction = budget * 0.1
  for (score, place) in secondary_attractions:
    if budget_for_secondary_attraction >= place["avg_price"]:
      budget -= place["avg_price"]
      recommended_secondary_attractions += 1

  return {
      "primary": { "data": primary_attractions, "recommended": recommended_primary_attractions },
      "secondary": { "data": secondary_attractions, "recommended": recommended_secondary_attractions },
      "food": { "data": food_places, "recommended": recommended_food_places},
      "accomodations": { "data": accomodations, "recommended": recommended_accomodations }
  }


places = generate_recommendations(data, from_date, to_date, moods, budget)

print("="*20)
print("Primary Attractions")
print("="*20)
for i, data in enumerate(places["primary"]["data"]):
  print(json.dumps(data, indent=2))
  if i >= places["primary"]["recommended"]:
    break

print("="*20)
print("Secondary Attractions")
print("="*20)
for i, data in enumerate(places["secondary"]["data"]):
  print(json.dumps(data, indent=2))
  if i >= places["secondary"]["recommended"]:
    break

print("="*20)
print("Foods")
print("="*20)
for i, data in enumerate(places["food"]["data"]):
  print(json.dumps(data, indent=2))
  if i >= places["food"]["recommended"]:
    break

print("="*20)
print("Accomodations")
print("="*20)
for i, data in enumerate(places["accomodations"]["data"]):
  print(json.dumps(data, indent=2))
  if i >= places["accomodations"]["recommended"]:
    break
