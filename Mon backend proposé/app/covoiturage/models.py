from app.extensions import db
from app.auth.models import User  # Import du modèle User
from datetime import datetime
import enum

class DayOfWeek(enum.Enum):
    MONDAY = 'Lundi'
    TUESDAY = 'Mardi'
    WEDNESDAY = 'Mercredi'
    THURSDAY = 'Jeudi'
    FRIDAY = 'Vendredi'
    SATURDAY = 'Samedi'
    SUNDAY = 'Dimanche'

class TripStatus(enum.Enum):
    PENDING = 'pending'     # En attente de passagers/conducteurs
    ACTIVE = 'active'       # Trajet en cours / validé
    COMPLETED = 'completed' # Trajet terminé
    CANCELLED = 'cancelled' # Trajet annulé

class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Lieu de départ et d'arrivée
    start_location = db.Column(db.String(255), nullable=False)
    end_location = db.Column(db.String(255), nullable=False)
    # Coordonnées géographiques (plus précises pour le matching)
    start_latitude = db.Column(db.Float, nullable=True)
    start_longitude = db.Column(db.Float, nullable=True)
    end_latitude = db.Column(db.Float, nullable=True)
    end_longitude = db.Column(db.Float, nullable=True)

    # Date et heure du trajet
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time_estimate = db.Column(db.DateTime, nullable=True) # Estimation

    # Jours de la semaine pour les trajets récurrents (ex: "Lundi,Mardi,Vendredi")
    recurring_days = db.Column(db.String(100), nullable=True)

    available_seats = db.Column(db.Integer, nullable=False)
    price_per_passenger = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(TripStatus), default=TripStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    driver_relationship = db.relationship(
        'User',
        back_populates='offered_rides',
        lazy=True,
        foreign_keys=[driver_id]
    )
    
    bookings_on_offer = db.relationship(
        'Booking',
        back_populates='offer',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            'id': self.id,
            'driver_id': self.driver_id,
            'driver_name': f"{self.driver.first_name} {self.driver.last_name}",
            'start_location': self.start_location,
            'end_location': self.end_location,
            'start_latitude': self.start_latitude,
            'start_longitude': self.start_longitude,
            'end_latitude': self.end_latitude,
            'end_longitude': self.end_longitude,
            'departure_time': self.departure_time.isoformat() if self.departure_time else None,
            'arrival_time_estimate': self.arrival_time_estimate.isoformat() if self.arrival_time_estimate else None,
            'recurring_days': self.recurring_days,
            'available_seats': self.available_seats,
            'price_per_passenger': self.price_per_passenger,
            'description': self.description,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_location = db.Column(db.String(255), nullable=False)
    end_location = db.Column(db.String(255), nullable=False)
    # Coordonnées géographiques
    start_latitude = db.Column(db.Float, nullable=True)
    start_longitude = db.Column(db.Float, nullable=True)
    end_latitude = db.Column(db.Float, nullable=True)
    end_longitude = db.Column(db.Float, nullable=True)

    # Date et heure souhaitées
    desired_departure_time = db.Column(db.DateTime, nullable=False)
    desired_arrival_time_latest = db.Column(db.DateTime, nullable=True) # Heure d'arrivée au plus tard

    # Jours de la semaine pour les demandes récurrentes
    recurring_days = db.Column(db.String(100), nullable=True)

    number_of_passengers = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.Enum(TripStatus), default=TripStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    passenger = db.relationship('User', backref=db.backref('requests', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'passenger_id': self.passenger_id,
            'passenger_name': f"{self.passenger.first_name} {self.passenger.last_name}", # Ajout du nom du passager
            'start_location': self.start_location,
            'end_location': self.end_location,
            'start_latitude': self.start_latitude,
            'start_longitude': self.start_longitude,
            'end_latitude': self.end_latitude,
            'end_longitude': self.end_longitude,
            'desired_departure_time': self.desired_departure_time.isoformat() if self.desired_departure_time else None,
            'desired_arrival_time_latest': self.desired_arrival_time_latest.isoformat() if self.desired_arrival_time_latest else None,
            'recurring_days': self.recurring_days,
            'number_of_passengers': self.number_of_passengers,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id'), nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False, default=1) # Nombre de places réservées
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Permet d'accéder à l'objet Offer ou User directement depuis un Booking
    offer = db.relationship('Offer', back_populates='bookings_on_offer', lazy=True, cascade="all")

    passenger_relationship = db.relationship(
        'User',
        back_populates='passenger_bookings',
        lazy=True,
        foreign_keys=[passenger_id]
    )

    def to_dict(self):
        return {
            'id': self.id,
            'offer_id': self.offer_id,
            'passenger_id': self.passenger_id,
            'seats_booked': self.seats_booked,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }