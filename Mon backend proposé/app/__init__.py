from flask import Flask
from app.extensions import db, migrate, cors, jwt

#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
#from flask_cors import CORS
#from flask_jwt_extended import JWTManager

import os
from dotenv import load_dotenv

#db = SQLAlchemy()
#migrate = Migrate()
#cors = CORS()
#jwt = JWTManager()

def create_app():
    
    print("--- Entrée dans create_app() ---") # Debug print
    
    # Charger les variables d'environnement depuis .env et .flaskenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.flaskenv'))
    
    print(f"--- .env et .flaskenv chargés ---") # Debug print
    
    app = Flask(__name__)

    # Configuration de l'application
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    print(f"DATABASE_URL de .env: {os.getenv('DATABASE_URL')}") # Debug print
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    # Pour ne pas afficher la clé secrète en clair dans les logs
    print(f"JWT_SECRET_KEY de .env: {'<DÉFINIE>' if os.getenv('JWT_SECRET_KEY') else '<NON DÉFINIE>'}") # Debug print
    app.config["CORS_HEADERS"] = 'Content-Type' # Pour les requêtes POST/PUT/DELETE avec CORS

    # Initialiser les extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    #cors.init_app(app, resources={r"/api/*": {"origins": cors_origins}})

    # Configurer CORS
    print(f"Avant de définir cors_origins. CORS_ORIGINS de .env: {os.getenv('CORS_ORIGINS')}") # Debug print

    # Ajout d'une gestion plus robuste pour cors_origins
    cors_origins_env_value = os.getenv("CORS_ORIGINS", "") # Récupère la valeur, vide si non définie
    if cors_origins_env_value:
        cors_origins = cors_origins_env_value.split(',')
    else:
        cors_origins = ["*"] # Valeur par défaut si rien n'est dans .env ou est vide

    print(f"Valeur finale de cors_origins: {cors_origins}") # Debug print

    try:
        cors.init_app(app, resources={r"/api/*": {"origins": cors_origins}})
        print("--- CORS initialisé avec succès ---") # Debug print
    except Exception as e:
        print(f"Erreur lors de l'initialisation de CORS: {e}") # Debug print
        raise # Rélance l'exception pour voir le traceback complet si l'erreur est là


    # Importer et enregistrer les Blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.covoiturage import bp as covoiturage_bp
    app.register_blueprint(covoiturage_bp, url_prefix='/covoiturage')

    from app.messaging import bp as messaging_bp
    app.register_blueprint(messaging_bp, url_prefix='/messaging')


    # Point de terminaison de test simple
    @app.route('/')
    def hello_world():
        return 'Hello from Flask Backend!'
    
    print("--- Fin de create_app() ---") # Debug print
    return app
