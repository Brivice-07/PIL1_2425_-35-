from flask import Blueprint, request, jsonify
from app import db
from models.models import Conducteur

conducteur_bp = Blueprint('conducteur', __name__)

@conducteur_bp.route('/ajouter', methods=["POST"])
def ajouter_conducteur():
    data = request.get_json()
    if not all(k in data for k in ["latitude", "longitude", "places"]):
        return jsonify({"error": "Données incomplètes"}), 400

    existe = Conducteur.query.filter_by(latitude=data['latitude'], longitude=data['longitude']).first()
    if existe:
        return jsonify({"error": "Conducteur déjà enregistré"}), 400

    try:
        conducteur = Conducteur(
            latitude=data['latitude'],
            longitude=data['longitude'],
            places_disponibles=data['places']
        )
        db.session.add(conducteur)
        db.session.commit()
        return jsonify({"message": "Conducteur ajouté avec succès"}), 201
    except Exception as e:
        return jsonify({"error": "Erreur lors de l'ajout"}), 500

@conducteur_bp.route('/liste', methods=["GET"])
def liste_conducteurs():
    conducteurs = Conducteur.query.all()
    return jsonify([
        {
            "id": c.id,
            "coordonnees": (c.latitude, c.longitude),
            "places_disponibles": c.places_disponibles
        } for c in conducteurs
    ])
