import json

def parsejsontodb():
    with open('places_with_coordinates.json', 'r') as file:
        data = json.load(file)
        print(data)

parsejsontodb();