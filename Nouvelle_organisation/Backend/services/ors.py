import openrouteservice
from flask import current_app

def get_distance_km_duree_min(start, via):
    try:
        client = openrouteservice.Client(key=current_app.config["ORS_API_KEY"])
        result = client.directions([start, via], profile='driving-car', format='geojson')
        segment = result['routes'][0]['segments'][0]
        return segment['distance'] / 1000, segment['duration'] / 60
    except Exception as e:
        print("Erreur ORS:", e)
        return float('inf'), float('inf')
