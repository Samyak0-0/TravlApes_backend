import json

import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

query = """
[out:json][timeout:120];
area["name"="Kathmandu"]["boundary"="administrative"]->.ktm;
area["name"="Lalitpur"]["boundary"="administrative"]->.lalitpur;
area["name"="Bhaktapur"]["boundary"="administrative"]->.bhaktapur;
(.ktm;.lalitpur;.bhaktapur;)->.valley;

(
  node["tourism"](area.valley);
  node["amenity"](area.valley);
  node["historic"](area.valley);
  node["natural"](area.valley);
);

out body;
"""

resp = requests.post(
    OVERPASS_URL, data=query, headers={"Content-Type": "text/plain"}, timeout=120
)

resp.raise_for_status()
data = resp.json()

places = []

for el in data.get("elements", []):
    tags = el.get("tags", {})
    name = tags.get("name")

    # Skip unnamed places (very important)
    if not name:
        continue

    place = {
        "osm_id": el["id"],
        "osm_type": el["type"],  # node
        "name": name,
        "latitude": el.get("lat"),
        "longitude": el.get("lon"),
        "tags": tags,
        "source": "OpenStreetMap",
    }

    places.append(place)

# Save to JSON file
output = {"region": "Kathmandu Valley", "count": len(places), "places": places}

with open("kathmandu_valley_places.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Saved {len(places)} places to kathmandu_valley_places.json")
