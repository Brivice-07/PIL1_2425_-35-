from flask import Blueprint, request, jsonify
from app.extensions import db
from app.auth.models import User, UserRole # Import du modèle User
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('users', __name__)

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user_profile(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"msg": "Unauthorized to update this user's profile"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    if 'role' in data:
        try:
            user.role = UserRole(data['role'])
        except ValueError:
            return jsonify({"msg": "Invalid role value. Must be 'passenger' or 'driver'."}), 400

    # Mise à jour des champs modifiables 
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.email = data.get('email', user.email) # Faites attention à la validation d'unicité ici si modifié
    # Si le rôle est modifiable 
    if 'role' in data:
        try:
            user.role = UserRole(data['role'])
        except ValueError:
            return jsonify({"msg": "Invalid role specified"}), 400

    user.profile_picture = data.get('profile_picture', user.profile_picture)
    user.home_address = data.get('home_address', user.home_address)
    user.habitual_departure_time = data.get('habitual_departure_time', user.habitual_departure_time)
    user.habitual_arrival_time = data.get('habitual_arrival_time', user.habitual_arrival_time)
    user.vehicle_make = data.get('vehicle_make', user.vehicle_make)
    user.vehicle_model = data.get('vehicle_model', user.vehicle_model)
    user.vehicle_seats_available = data.get('vehicle_seats_available', user.vehicle_seats_available)

    try:
        db.session.commit()
        return jsonify({"msg": "Profile updated successfully", "user": user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500