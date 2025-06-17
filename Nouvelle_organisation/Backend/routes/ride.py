from flask import Blueprint, request, jsonify, current_app
from app import db
from models.models import RideRequest, Conducteur
from services.ors import get_distance_km_duree_min

ride_bp = Blueprint('ride', __name__)

IFRI_COORD = [2.4245, 6.3624]

@ride_bp.route('/request', methods=["POST"])
def request_ride():
    data = request.get_json()
    if not data or 'user' not in data or 'origin' not in data or 'destination' not in data:
        return jsonify({"error": "Champs manquants"}), 400

    ride = RideRequest(
        user=data['user'],
        origin=data['origin'],
        destination=data['destination']
    )
    db.session.add(ride)
    db.session.commit()
    return jsonify({"message": "Trajet enregistré", "ride_id": ride.id}), 201

@ride_bp.route('/match', methods=["POST"])
def match_passager():
    data = request.get_json()
    try:
        depart = tuple(data.get('depart'))
    except:
        return jsonify({"error": "Coordonnées invalides"}), 400

    conducteurs = Conducteur.query.all()
    matches = []

    for c in conducteurs:
        if c.places_disponibles == 0:
            continue
        distance_depart, _ = get_distance_km_duree_min(depart, (c.latitude, c.longitude))
        if distance_depart <= c.distance_max_detour:
            matches.append({
                "conducteur_id": c.id,
                "nom": c.nom,
                "photo": c.photo_profil,
                "heure_depart": c.heure_depart,
                "itineraire": f"{depart} → {IFRI_COORD}",
                "places_disponibles": c.places_disponibles
            })
    return jsonify(matches)

@ride_bp.route('/confirm', methods=["POST"])
def confirm_ride():
    data = request.get_json()
    ride = RideRequest.query.get(data.get('ride_id'))
    if not ride:
        return jsonify({"error": "Ride non trouvé"}), 404
    ride.status = "confirmed"
    db.session.commit()
    return jsonify({"message": "Trajet confirmé"})

@ride_bp.route('/cancel', methods=["POST"])
def cancel_ride():
    data = request.get_json()
    ride = RideRequest.query.get(data.get('ride_id'))
    if not ride:
        return jsonify({"error": "Ride non trouvé"}), 404
    ride.status = "cancelled"
    db.session.commit()
    return jsonify({"message": "Trajet annulé"})

@ride_bp.route('/status', methods=["GET"])
def ride_status():
    ride_id = request.args.get('ride_id')
    ride = RideRequest.query.get(ride_id)
    if not ride:
        return jsonify({"error": "Ride non trouvé"}), 404
    return jsonify({
        "ride_id": ride.id,
        "user": ride.user,
        "origin": ride.origin,
        "destination": ride.destination,
        "status": ride.status
    })
