from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models.user_model import Utilisateur
from app.extensions import db

register_bp = Blueprint('register', __name__)

@register_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()

    nom = data.get('nom')
    prenoms = data.get('prenoms')
    email = data.get('email')
    telephone = data.get('telephone')
    mot_de_passe = data.get('mot_de_passe')
    statut = data.get('statut')

    # Vérifie si email ou téléphone existe déjà
    if Utilisateur.query.filter((Utilisateur.email == email) | (Utilisateur.telephone == telephone)).first():
        return jsonify({'error': 'Email ou téléphone déjà utilisé'}), 400

    utilisateur = Utilisateur(
        nom=nom,
        prenoms=prenoms,
        email=email,
        telephone=telephone,
        mot_de_passe=generate_password_hash(mot_de_passe),
        statut=statut
    )
    db.session.add(utilisateur)
    db.session.commit()

    return jsonify({'message': 'Inscription réussie'}), 201
