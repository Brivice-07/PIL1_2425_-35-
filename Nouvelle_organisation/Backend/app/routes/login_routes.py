from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from ..models.user_model import Utilisateur
from flask_jwt_extended import create_access_token
from datetime import timedelta
from sqlalchemy import or_

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])  
def api_login():
    data = request.get_json()  
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')

    utilisateur = Utilisateur.query.filter(
    or_(Utilisateur.email == email, Utilisateur.telephone == email)
).first()

    if utilisateur and check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
        access_token = create_access_token(identity={
            'id': utilisateur.id,
            'email': utilisateur.email,
            'statut': utilisateur.statut
        }, expires_delta=timedelta(days=1))
        
        return jsonify({'token': access_token, 'message': 'Connexion réussie'}), 200
        
    else:
        return jsonify({'error': 'Identifiants incorrects'}), 401
