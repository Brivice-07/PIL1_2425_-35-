from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user_model import Utilisateur  # Assure-toi que le chemin est bon

home_bp = Blueprint('home', __name__)

@home_bp.route('/api/home', methods=['GET'])
@jwt_required()
def home():
    current_identity = get_jwt_identity()  # ex: {'id': 1, 'email': '...'}
    user_id = current_identity.get('id')

    utilisateur = Utilisateur.query.get(user_id)

    if not utilisateur:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404

    user_data = {
        'id': utilisateur.id,
        'nom': utilisateur.nom,
        'prenoms': utilisateur.prenoms,
        'email': utilisateur.email,
        'statut': utilisateur.statut,
        'profil': utilisateur.profil,
        'point_de_depart': utilisateur.point_de_depart,
        'horaires': utilisateur.horaires
    }

    return jsonify({
        'message': 'Bienvenue dans votre profil',
        'utilisateur': user_data
    }), 200
