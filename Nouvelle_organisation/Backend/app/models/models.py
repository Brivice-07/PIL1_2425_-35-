from ..extensions import db

class RideRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), nullable=False)
    origin = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default="pending")

class Conducteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    places_disponibles = db.Column(db.Integer, nullable=False)
    distance_max_detour = db.Column(db.Float, default=5.0)
    nom = db.Column(db.String(100))
    photo_profil = db.Column(db.String(255))
    heure_depart = db.Column(db.String(50))
