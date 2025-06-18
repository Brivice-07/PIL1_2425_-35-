from flask import Blueprint, request, jsonify
from app.extensions import db, jwt
from app.auth.models import User, UserRole
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

print("--- Executing app/auth/routes.py ---")
bp = Blueprint('auth', __name__)
print("--- Blueprint 'bp' defined in app/auth/routes.py ---")

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')
    role_str = data.get('role', 'passenger') # Rôle par défaut 'passenger' 

    # Vérification des champs obligatoires 
    if not all([first_name, last_name, email, phone_number, password]):
        return jsonify({"msg": "Missing required fields"}), 400

    # Validation du rôle
    try:
        role = UserRole(role_str.lower())
    except ValueError:
        return jsonify({"msg": "Invalid role specified. Must be 'passenger' or 'driver'"}), 400

    # Vérification de l'unicité de l'e-mail et du numéro de téléphone 
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 409
    if User.query.filter_by(phone_number=phone_number).first():
        return jsonify({"msg": "Phone number already exists"}), 409

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        role=role
    )
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User registered successfully", "user_id": new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"An error occurred: {str(e)}"}), 500

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # L'utilisateur peut se connecter avec email ou numéro de téléphone 
    identifier = data.get('identifier') # Peut être email ou phone_number
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"msg": "Missing identifier or password"}), 400

    user = User.query.filter(
        (User.email == identifier) | (User.phone_number == identifier)
    ).first()

    # Gestion des erreurs de connexion 
    if user is None or not user.check_password(password):
        return jsonify({"msg": "Bad username or password"}), 401

    # Création du token JWT
    access_token = create_access_token(
        identity=user.id,
        expires_delta=datetime.timedelta(hours=1) # Token valable 1 heure
    )
    return jsonify(access_token=access_token, user_id=user.id, role=user.role.value), 200

# Exemple de route protégée par JWT (pour tester)
@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200