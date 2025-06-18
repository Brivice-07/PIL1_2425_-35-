from flask import Blueprint, request, jsonify
from app.extensions import db
from app.covoiturage.models import Offer, Request, TripStatus, Booking
from app.covoiturage.matching_algo import find_matches, find_offers_for_request
from app.auth.models import User, UserRole # Pour vérifier le rôle du user
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('covoiturage', __name__)

# --- Offres (Conducteurs) ---

@bp.route('/offers', methods=['POST'])
@jwt_required()
def create_offer():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != UserRole.DRIVER: # Un conducteur PUR
        return jsonify({"msg": "Only users with 'driver' role can create offers"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # Valider les données d'entrée
    required_fields = ['start_location', 'end_location', 'departure_time', 'available_seats', 'price_per_passenger']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields for offer"}), 400

    try:
        # Convertir la chaîne de temps en objet datetime
        departure_time_dt = datetime.fromisoformat(data['departure_time'])
        # Exemple de gestion de l'heure d'arrivée estimée
        arrival_time_estimate_dt = datetime.fromisoformat(data['arrival_time_estimate']) if 'arrival_time_estimate' in data else None

        new_offer = Offer(
            driver_id=current_user_id,
            start_location=data['start_location'],
            end_location=data['end_location'],
            start_latitude=data.get('start_latitude'),
            start_longitude=data.get('start_longitude'),
            end_latitude=data.get('end_latitude'),
            end_longitude=data.get('end_longitude'),
            departure_time=departure_time_dt,
            arrival_time_estimate=arrival_time_estimate_dt,
            recurring_days=data.get('recurring_days'),
            available_seats=data['available_seats'],
            price_per_passenger=data['price_per_passenger'],
            description=data.get('description'),
            status=TripStatus.PENDING # Nouvelle offre est en attente
        )
        db.session.add(new_offer)
        db.session.commit()
        return jsonify({"msg": "Offer created successfully", "offer": new_offer.to_dict()}), 201
    except ValueError as ve:
        return jsonify({"msg": f"Invalid date/time format: {str(ve)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

@bp.route('/offers', methods=['GET'])
@jwt_required()
def get_all_offers():
    # Optionnellement, filtrer par utilisateur, statut, etc.
    offers = Offer.query.filter_by(status=TripStatus.PENDING).all() # Seulement les offres en attente
    return jsonify([offer.to_dict() for offer in offers]), 200

@bp.route('/offers/<int:offer_id>', methods=['GET'])
@jwt_required()
def get_offer(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({"msg": "Offer not found"}), 404
    return jsonify(offer.to_dict()), 200

# Endpoint pour filtrer les offres (très basique pour l'instant)
@bp.route('/offers/search', methods=['GET'])
@jwt_required()
def search_offers():
    # Exemple de paramètres de recherche
    start_loc = request.args.get('start_location')
    end_loc = request.args.get('end_location')
    date_str = request.args.get('date') # Format 'YYYY-MM-DD'

    query = Offer.query.filter_by(status=TripStatus.PENDING)

    if start_loc:
        query = query.filter(Offer.start_location.ilike(f'%{start_loc}%')) # ilike pour recherche insensible à la casse
    if end_loc:
        query = query.filter(Offer.end_location.ilike(f'%{end_loc}%'))
    if date_str:
        try:
            search_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            # Filtrer les offres dont la date de départ correspond à la date de recherche
            query = query.filter(db.func.date(Offer.departure_time) == search_date)
        except ValueError:
            return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD."}), 400

    offers = query.all()
    return jsonify([offer.to_dict() for offer in offers]), 200


# --- Demandes (Passagers) ---

@bp.route('/requests', methods=['POST'])
@jwt_required()
def create_request():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != UserRole.PASSENGER: # Un passager PUR
        return jsonify({"msg": "Only users with 'passenger' role can create requests"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    required_fields = ['start_location', 'end_location', 'desired_departure_time', 'number_of_passengers']
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields for request"}), 400

    try:
        desired_departure_time_dt = datetime.fromisoformat(data['desired_departure_time'])
        desired_arrival_time_latest_dt = datetime.fromisoformat(data['desired_arrival_time_latest']) if 'desired_arrival_time_latest' in data else None

        new_request = Request(
            passenger_id=current_user_id,
            start_location=data['start_location'],
            end_location=data['end_location'],
            start_latitude=data.get('start_latitude'),
            start_longitude=data.get('start_longitude'),
            end_latitude=data.get('end_latitude'),
            end_longitude=data.get('end_longitude'),
            desired_departure_time=desired_departure_time_dt,
            desired_arrival_time_latest=desired_arrival_time_latest_dt,
            recurring_days=data.get('recurring_days'),
            number_of_passengers=data['number_of_passengers'],
            status=TripStatus.PENDING
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({"msg": "Request created successfully", "request": new_request.to_dict()}), 201
    except ValueError as ve:
        return jsonify({"msg": f"Invalid date/time format: {str(ve)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

@bp.route('/requests', methods=['GET'])
@jwt_required()
def get_all_requests():
    requests = Request.query.filter_by(status=TripStatus.PENDING).all()
    return jsonify([req.to_dict() for req in requests]), 200

@bp.route('/requests/<int:request_id>', methods=['GET'])
@jwt_required()
def get_request(request_id):
    req = Request.query.get(request_id)
    if not req:
        return jsonify({"msg": "Request not found"}), 404
    return jsonify(req.to_dict()), 200


# --- Routes pour les Réservations (Bookings) ---

# POST /api/covoiturage/offers/<int:offer_id>/book
# Permet à un passager de réserver une ou plusieurs places sur une offre.
@bp.route('/offers/<int:offer_id>/book', methods=['POST'])
@jwt_required()
def book_ride_offer(offer_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    seats_to_book = data.get('seats_booked', 1) # Par défaut, on réserve 1 place

    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({"msg": "Offer not found"}), 404

    # L'utilisateur ne peut pas réserver sa propre offre
    if offer.driver_id == current_user_id:
        return jsonify({"msg": "You cannot book your own offer"}), 400

    # Vérifier si l'utilisateur est un passager
    user = User.query.get(current_user_id)
    if not user or user.role != UserRole.PASSENGER:
        return jsonify({"msg": "Only users with 'passenger' role can book offers"}), 403

    if seats_to_book <= 0:
        return jsonify({"msg": "Number of seats must be positive"}), 400

    if seats_to_book > offer.available_seats:
        return jsonify({"msg": f"Not enough available seats. Only {offer.available_seats} remaining."}), 400

    # Vérifier si l'utilisateur a déjà une réservation en cours pour cette offre
    existing_booking = Booking.query.filter_by(offer_id=offer_id, passenger_id=current_user_id, status='pending').first()
    if existing_booking:
        return jsonify({"msg": "You already have a pending booking for this offer. Update it instead."}), 400

    new_booking = Booking(
        offer_id=offer_id,
        passenger_id=current_user_id,
        seats_booked=seats_to_book,
        status='pending' # Le statut initial est 'en attente'
    )
    db.session.add(new_booking)

    # Décrémenter le nombre de places disponibles sur l'offre
    offer.available_seats -= seats_to_book
    db.session.commit()

    return jsonify({"msg": "Booking created successfully", "booking": new_booking.to_dict()}), 201

# GET /api/covoiturage/my_bookings
# Récupère toutes les réservations faites par l'utilisateur actuel (en tant que passager)
@bp.route('/my_bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    current_user_id = get_jwt_identity()
    bookings = Booking.query.filter_by(passenger_id=current_user_id).all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

# GET /api/covoiturage/offers/<int:offer_id>/bookings
# Permet au conducteur de voir les réservations pour son offre spécifique.
@bp.route('/offers/<int:offer_id>/bookings', methods=['GET'])
@jwt_required()
def get_bookings_for_offer(offer_id):
    current_user_id = get_jwt_identity()
    offer = Offer.query.get(offer_id)

    if not offer:
        return jsonify({"msg": "Offer not found"}), 404

    # S'assurer que seul le conducteur de l'offre peut voir les réservations
    if offer.driver_id != current_user_id:
        return jsonify({"msg": "Unauthorized to view bookings for this offer"}), 403

    bookings = Booking.query.filter_by(offer_id=offer_id).all()
    return jsonify([booking.to_dict() for booking in bookings]), 200

# PUT /api/covoiturage/bookings/<int:booking_id>/status
# Permet de mettre à jour le statut d'une réservation (ex: 'confirmed', 'cancelled')
# Peut être utilisé par le passager pour annuler, ou le conducteur pour confirmer
@bp.route('/bookings/<int:booking_id>/status', methods=['PUT'])
@jwt_required()
def update_booking_status(booking_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    new_status = data.get('status')

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"msg": "Booking not found"}), 404

    # Vérifier l'autorisation
    offer = Offer.query.get(booking.offer_id)
    if not offer: # Devrait pas arriver si FK est bonne
        return jsonify({"msg": "Associated offer not found"}), 500

    is_passenger = booking.passenger_id == current_user_id
    is_driver = offer.driver_id == current_user_id

    if not is_passenger and not is_driver:
        return jsonify({"msg": "Unauthorized to update this booking"}), 403

    # Logique de changement de statut
    if new_status == 'cancelled':
        # Le passager ou le conducteur peut annuler
        if booking.status != 'cancelled': # Éviter de double annuler
            booking.status = 'cancelled'
            offer.available_seats += booking.seats_booked # Remettre les places
            db.session.commit()
            return jsonify({"msg": "Booking cancelled successfully", "booking": booking.to_dict()}), 200
        else:
            return jsonify({"msg": "Booking is already cancelled"}), 400
    elif new_status == 'confirmed':
        # Seul le conducteur peut confirmer
        if is_driver:
            if booking.status == 'pending':
                booking.status = 'confirmed'
                db.session.commit()
                return jsonify({"msg": "Booking confirmed successfully", "booking": booking.to_dict()}), 200
            else:
                return jsonify({"msg": f"Booking cannot be confirmed from status: {booking.status}"}), 400
        else:
            return jsonify({"msg": "Only the driver can confirm a booking"}), 403
    else:
        return jsonify({"msg": "Invalid or unsupported status"}), 400

# DELETE /api/covoiturage/bookings/<int:booking_id>
# Permet d'annuler et de supprimer une réservation (peut être après confirmation par le conducteur).

@bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def delete_booking(booking_id):
    current_user_id = get_jwt_identity()
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"msg": "Booking not found"}), 404

    offer = Offer.query.get(booking.offer_id)
    if not offer: # Devrait pas arriver si FK est bonne
        return jsonify({"msg": "Associated offer not found"}), 500

    # Seul le passager qui a fait la réservation ou le conducteur de l'offre peut supprimer
    if booking.passenger_id != current_user_id and offer.driver_id != current_user_id:
        return jsonify({"msg": "Unauthorized to delete this booking"}), 403

    # Si la réservation n'est pas déjà annulée, remettre les places disponibles
    if booking.status != 'cancelled':
        offer.available_seats += booking.seats_booked

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"msg": "Booking deleted"}), 200


# --- Matching Offres et Demandes ---
@bp.route('/offers/<int:offer_id>/matches', methods=['GET'])
@jwt_required()
def get_offer_matches(offer_id):
    current_user_id = get_jwt_identity()
    offer = Offer.query.get(offer_id)

    if not offer:
        return jsonify({"msg": "Offer not found"}), 404
    # S'assurer que seul le conducteur de l'offre peut voir les matchs (ou un admin)
    if offer.driver_id != current_user_id:
        return jsonify({"msg": "Unauthorized to view matches for this offer"}), 403

    # Appel de l'algorithme de matching
    radius_km = float(request.args.get('radius', 5))
    time_tolerance_minutes = int(request.args.get('time_tolerance', 30))

    matching_requests = find_matches(offer, radius_km, time_tolerance_minutes)

    return jsonify([req.to_dict() for req in matching_requests]), 200

@bp.route('/requests/<int:request_id>/matches', methods=['GET'])
@jwt_required()
def get_request_matches(request_id):
    current_user_id = get_jwt_identity()
    req = Request.query.get(request_id)

    if not req:
        return jsonify({"msg": "Request not found"}), 404
    # S'assurer que seul le passager de la demande peut voir les matchs (ou un admin)
    if req.passenger_id != current_user_id:
        return jsonify({"msg": "Unauthorized to view matches for this request"}), 403

    radius_km = float(request.args.get('radius', 5))
    time_tolerance_minutes = int(request.args.get('time_tolerance', 30))

    matching_offers = find_offers_for_request(req, radius_km, time_tolerance_minutes)

    return jsonify([offer.to_dict() for offer in matching_offers]), 200

