import json
import time

import requests

INPUT_FILE = "kathmandu_places.json"
OUTPUT_FILE = "places_with_coordinates.json"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "NepalTravelApp/1.0 (hehe@gmail.com)"}


def geocode_place(name):
    params = {"q": f"{name}, Kathmandu, Nepal", "format": "json", "limit": 1}

    resp = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=20)

    resp.raise_for_status()
    data = resp.json()

    if not data:
        return None, None

    return float(data[0]["lat"]), float(data[0]["lon"])


# ---- Load input JSON ----
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

places = data["places"]

# ---- Geocode each place ----
for place in places:
    name = place["name"]
    print(f"Geocoding: {name}")

    lat, lon = geocode_place(name)

    place["latitude"] = lat
    place["longitude"] = lon

    time.sleep(1)  # IMPORTANT: respect Nominatim rate limits

# ---- Save output JSON ----
output = {
    "metadata": {
        "source": "Nominatim (OpenStreetMap)",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_places": len(places),
    },
    "places": places,
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nSaved coordinates to {OUTPUT_FILE}")

