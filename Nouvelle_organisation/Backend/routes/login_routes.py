from flask import Blueprint, request, redirect, session, flash, url_for
from werkzeug.security import check_password_hash
from models.user_model import Utilisateur

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    mot_de_passe = request.form.get('mot_de_passe')

    utilisateur = Utilisateur.query.filter_by(email=email).first()

    if utilisateur and check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
        session['user_id'] = utilisateur.id
        session['statut'] = utilisateur.statut
        flash("Connexion réussie", "success")
        return redirect(url_for('home.home'))  # redirige vers la page d'accueil
    else:
        flash("Identifiants incorrects", "danger")
        return redirect('/login')