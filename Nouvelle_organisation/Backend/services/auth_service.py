from models.user_model import db, User
from flask_jwt_extended import create_access_token
from datetime import timedelta

def register_user(data):
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'Email déjà utilisé'}, 400

    user = User(
        nom=data['nom'],
        prenoms=data['prenoms'],
        email=data['email'],
        telephone=data['telephone'],
        statut=data['statut'],
        point_de_depart=data.get('point_de_depart'),
        horaires=data.get('horaires')
    )
    user.set_password(data['mot_de_passe'])
    db.session.add(user)
    db.session.commit()
    return {'message': 'Inscription réussie'}, 201

def login_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['mot_de_passe']):
        return {'error': 'Identifiants incorrects'}, 401

    access_token = create_access_token(identity={
        'id': user.id,
        'email': user.email,
        'statut': user.statut
    }, expires_delta=timedelta(days=1))

    return {'token': access_token}, 200