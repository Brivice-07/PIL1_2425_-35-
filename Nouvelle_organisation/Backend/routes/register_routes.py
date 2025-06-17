from flask import Blueprint, request, redirect, flash
from werkzeug.security import generate_password_hash
from models.user_model import Utilisateur
from app import db

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    nom = request.form.get('nom')
    prenoms = request.form.get('prenoms')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    mot_de_passe = request.form.get('mot_de_passe')
    statut = request.form.get('statut')

    if Utilisateur.query.filter((Utilisateur.email == email) | (Utilisateur.telephone == telephone)).first():
        flash("Email ou téléphone déjà utilisé", "danger")
        return redirect('/register')

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

    flash("Inscription réussie", "success")
    return redirect('/login')