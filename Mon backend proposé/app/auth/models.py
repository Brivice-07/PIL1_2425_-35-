from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from datetime import datetime

# Enum pour les rôles utilisateur 
class UserRole(enum.Enum):
    DRIVER = 'driver'
    PASSENGER = 'passenger'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.PASSENGER, nullable=False) # Rôle par défaut
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    profile_picture = db.Column(db.String(255), nullable=True) # URL vers l'image 
    # Point de départ habituel (adresse détaillée ou coordonnées géo.)
    home_address = db.Column(db.String(255), nullable=True)
    # Horaires de départ et d'arrivée habituels 
    habitual_departure_time = db.Column(db.String(50), nullable=True)
    habitual_arrival_time = db.Column(db.String(50), nullable=True)

    # Informations sur le véhicule (si conducteur) 
    vehicle_make = db.Column(db.String(100), nullable=True)
    vehicle_model = db.Column(db.String(100), nullable=True)
    vehicle_seats_available = db.Column(db.Integer, nullable=True)

# Relations pour la messagerie
    conversations = db.relationship(
        'Conversation',
        secondary='conversation_participants',
        back_populates='participants'
    )
    # Messages envoyés par cet utilisateur
    sent_messages = db.relationship(
        'Message',
        back_populates='sender_relationship',
        lazy=True,
        foreign_keys='Message.sender_id'
    )
    received_messages = db.relationship('Message', back_populates='recipient_relationship', lazy=True, foreign_keys='Message.recipient_id')

# Relations pour le covoiturage
    offered_rides = db.relationship('Offer', back_populates='driver_relationship', lazy='dynamic', foreign_keys='Offer.driver_id')

    passenger_bookings = db.relationship('Booking', back_populates='passenger_relationship', lazy='dynamic', foreign_keys='Booking.passenger_id')

    def set_password(self, password):
        """Hache le mot de passe et le stocke."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie si le mot de passe fourni correspond au haché."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convertit l'objet User en dictionnaire (pour les réponses JSON)."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'role': self.role.value,
            'profile_picture': self.profile_picture,
            'home_address': self.home_address,
            'habitual_departure_time': self.habitual_departure_time,
            'habitual_arrival_time': self.habitual_arrival_time,
            'vehicle_make': self.vehicle_make,
            'vehicle_model': self.vehicle_model,
            'vehicle_seats_available': self.vehicle_seats_available,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<User {self.email}>'