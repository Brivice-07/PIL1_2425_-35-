from flask import Blueprint, session, redirect

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    return "Bienvenue sur la page d’accueil"