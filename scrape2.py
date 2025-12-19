import json
import time

import requests


def fetch_overpass_data(query, max_retries=3):
    """Fetch data from Overpass API with retry logic"""
    overpass_url = "http://overpass-api.de/api/interpreter"

    for attempt in range(max_retries):
        try:
            response = requests.post(overpass_url, data={"data": query}, timeout=180)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2**attempt
                print(f"Request failed: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts: {e}")
                return None


def process_elements(elements):
    """Process elements and return list of named places only"""
    places = []
    for element in elements:
        tags = element.get("tags", {})
        # Prefer English name, fall back to default name
        name = tags.get("name:en", tags.get("name", "")).strip()

        # Skip unnamed places
        if not name:
            continue

        lat = element.get("lat")
        lon = element.get("lon")

        # For ways, get center point
        if not lat or not lon:
            continue

        places.append({"name": name, "latitude": lat, "longitude": lon, "tags": tags})

    return places


def get_transport(bbox):
    """Fetch bus stops"""
    query = f"""
    [out:json][timeout:180];
    (
      node["highway"="bus_stop"]({bbox});
      node["amenity"="bus_station"]({bbox});
    );
    out body;
    """

    print("Fetching transport...")
    data = fetch_overpass_data(query)
    if not data:
        return []

    places = process_elements(data.get("elements", []))
    return [
        {"name": p["name"], "latitude": p["latitude"], "longitude": p["longitude"]}
        for p in places
    ]


def get_food_places(bbox):
    """Fetch restaurants, cafes, bars, etc."""
    query = f"""
    [out:json][timeout:180];
    (
      node["amenity"="restaurant"]({bbox});
      way["amenity"="restaurant"]({bbox});
      node["amenity"="cafe"]({bbox});
      way["amenity"="cafe"]({bbox});
      node["amenity"="fast_food"]({bbox});
      way["amenity"="fast_food"]({bbox});
      node["amenity"="bar"]({bbox});
      way["amenity"="bar"]({bbox});
      node["amenity"="pub"]({bbox});
      way["amenity"="pub"]({bbox});
      node["shop"="bakery"]({bbox});
    );
    out center;
    """

    print("Fetching food places...")
    data = fetch_overpass_data(query)
    if not data:
        return {"restaurants": [], "cafes": [], "bars": [], "bakeries": []}

    restaurants = []
    cafes = []
    bars = []
    bakeries = []

    for element in data.get("elements", []):
        tags = element.get("tags", {})
        # Prefer English name, fall back to default name
        name = tags.get("name:en", tags.get("name", "")).strip()

        if not name:
            continue

        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")

        if not lat or not lon:
            continue

        place = {"name": name, "latitude": lat, "longitude": lon}

        amenity = tags.get("amenity", "")
        shop = tags.get("shop", "")

        if amenity == "restaurant" or amenity == "fast_food":
            restaurants.append(place)
        elif amenity == "cafe":
            cafes.append(place)
        elif amenity in ["bar", "pub"]:
            bars.append(place)
        elif shop == "bakery":
            bakeries.append(place)

    return {
        "restaurants": restaurants,
        "cafes": cafes,
        "bars": bars,
        "bakeries": bakeries,
    }


def get_accommodations(bbox):
    """Fetch hotels, lodges, guest houses, hostels"""
    query = f"""
    [out:json][timeout:180];
    (
      node["tourism"="hotel"]({bbox});
      way["tourism"="hotel"]({bbox});
      node["tourism"="guest_house"]({bbox});
      way["tourism"="guest_house"]({bbox});
      node["tourism"="hostel"]({bbox});
      way["tourism"="hostel"]({bbox});
      node["tourism"="motel"]({bbox});
      way["tourism"="motel"]({bbox});
    );
    out center;
    """

    print("Fetching accommodations...")
    data = fetch_overpass_data(query)
    if not data:
        return []

    hotels = []
    lodges = []
    hostels = []

    for element in data.get("elements", []):
        tags = element.get("tags", {})
        # Prefer English name, fall back to default name
        name = tags.get("name:en", tags.get("name", "")).strip()

        if not name:
            continue

        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")

        if not lat or not lon:
            continue

        place = {"name": name, "latitude": lat, "longitude": lon}

        tourism_type = tags.get("tourism", "")

        if tourism_type == "hotel" or tourism_type == "motel":
            hotels.append(place)
        elif tourism_type == "guest_house":
            lodges.append(place)
        elif tourism_type == "hostel":
            hostels.append(place)

    return [{"hotel": hotels}, {"lodge": lodges}, {"hostel": hostels}]


def get_attractions(bbox):
    """Fetch various attractions"""
    query = f"""
    [out:json][timeout:180];
    (
      node["tourism"="gallery"]({bbox});
      way["tourism"="gallery"]({bbox});
      node["tourism"="museum"]({bbox});
      way["tourism"="museum"]({bbox});
      node["tourism"="attraction"]({bbox});
      way["tourism"="attraction"]({bbox});
      node["historic"]({bbox});
      way["historic"]({bbox});
      relation["historic"]({bbox});
      node["tourism"="zoo"]({bbox});
      way["tourism"="zoo"]({bbox});
      node["amenity"="nightclub"]({bbox});
      way["amenity"="nightclub"]({bbox});
      node["amenity"="place_of_worship"]["religion"="hindu"]({bbox});
      way["amenity"="place_of_worship"]["religion"="hindu"]({bbox});
      relation["amenity"="place_of_worship"]["religion"="hindu"]({bbox});
      node["amenity"="place_of_worship"]["religion"="buddhist"]({bbox});
      way["amenity"="place_of_worship"]["religion"="buddhist"]({bbox});
      relation["amenity"="place_of_worship"]["religion"="buddhist"]({bbox});
      node["natural"="water"]["water"="pond"]({bbox});
      way["natural"="water"]["water"="pond"]({bbox});
    );
    out center;
    """

    print("Fetching attractions...")
    data = fetch_overpass_data(query)
    if not data:
        return []

    art_gallery = []
    museum = []
    heritage = []
    zoo = []
    clubs = []
    temples = []
    ponds = []
    attractions = []

    for element in data.get("elements", []):
        tags = element.get("tags", {})
        # Prefer English name, fall back to default name
        name = tags.get("name:en", tags.get("name", "")).strip()

        if not name:
            continue

        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")

        if not lat or not lon:
            continue

        place = {"name": name, "latitude": lat, "longitude": lon}

        if tags.get("tourism") == "gallery":
            art_gallery.append(place)
        elif tags.get("tourism") == "museum":
            museum.append(place)
        elif tags.get("tourism") == "attraction":
            attractions.append(place)
        elif tags.get("historic"):
            heritage.append(place)
        elif tags.get("tourism") == "zoo":
            zoo.append(place)
        elif tags.get("amenity") == "nightclub":
            clubs.append(place)
        elif tags.get("amenity") == "place_of_worship":
            temples.append(place)
        elif tags.get("natural") == "water" and tags.get("water") == "pond":
            ponds.append(place)

    return [
        {"art_gallery": art_gallery},
        {"museum": museum},
        {"attractions": attractions},
        {"heritage": heritage},
        {"zoo": zoo},
        {"clubs": clubs},
        {"temples": temples},
        {"ponds": ponds},
    ]


def get_nature(bbox):
    """Fetch natural features"""
    query = f"""
    [out:json][timeout:180];
    (
      node["natural"="peak"]({bbox});
      node["natural"="water"]["water"="lake"]({bbox});
      way["natural"="water"]["water"="lake"]({bbox});
      way["waterway"="river"]({bbox});
      node["tourism"="viewpoint"]({bbox});
    );
    out center;
    """

    print("Fetching nature places...")
    data = fetch_overpass_data(query)
    if not data:
        return []

    peaks = []
    lakes = []
    rivers = []
    views = []

    for element in data.get("elements", []):
        tags = element.get("tags", {})
        # Prefer English name, fall back to default name
        name = tags.get("name:en", tags.get("name", "")).strip()

        if not name:
            continue

        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")

        if not lat or not lon:
            continue

        place = {"name": name, "latitude": lat, "longitude": lon}

        if tags.get("natural") == "peak":
            peaks.append(place)
        elif tags.get("natural") == "water" and tags.get("water") == "lake":
            lakes.append(place)
        elif tags.get("waterway") == "river":
            rivers.append(place)
        elif tags.get("tourism") == "viewpoint":
            views.append(place)

    return [{"peaks": peaks}, {"lakes": lakes}, {"rivers": rivers}, {"views": views}]


def main():
    print("Fetching POIs for Kathmandu Valley...\n")

    # Extended Kathmandu Valley bounding box covering all major areas
    # Includes Kathmandu, Lalitpur, Bhaktapur, and surrounding areas
    bbox = "27.55,85.15,27.85,85.55"

    # Fetch all data
    bus_stops = get_transport(bbox)
    time.sleep(1)

    food_data = get_food_places(bbox)
    time.sleep(1)

    accommodations = get_accommodations(bbox)
    time.sleep(1)

    attractions = get_attractions(bbox)
    time.sleep(1)

    nature = get_nature(bbox)

    # Build final structure
    final_data = {
        "bus_stop": bus_stops,
        "restaurants": food_data["restaurants"],
        "cafes": food_data["cafes"],
        "bars": food_data["bars"],
        "bakeries": food_data["bakeries"],
        "accommodations": accommodations,
        "attractions": attractions,
        "nature": nature,
    }

    # Save to file
    with open("kathmandu_pois.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Bus Stops: {len(bus_stops)}")
    print(f"Restaurants: {len(food_data['restaurants'])}")
    print(f"Cafes: {len(food_data['cafes'])}")
    print(f"Bars: {len(food_data['bars'])}")
    print(f"Bakeries: {len(food_data['bakeries'])}")

    for acc in accommodations:
        for key, value in acc.items():
            print(f"{key.capitalize()}: {len(value)}")

    for attr in attractions:
        for key, value in attr.items():
            print(f"{key.replace('_', ' ').capitalize()}: {len(value)}")

    for nat in nature:
        for key, value in nat.items():
            print(f"{key.capitalize()}: {len(value)}")

    print("\nData saved to kathmandu_pois.json")
    print("All unnamed places have been filtered out!")
    print("=" * 60)


if __name__ == "__main__":
    main()

