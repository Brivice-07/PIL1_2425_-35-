from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

home_bp = Blueprint('home', __name__)

@home_bp.route('/api/home', methods=['GET'])
@jwt_required()
def home():
    current_user = get_jwt_identity() 

    return jsonify({
        'message': 'Bienvenue sur la page d’accueil',
        'utilisateur': current_user
    }), 200
