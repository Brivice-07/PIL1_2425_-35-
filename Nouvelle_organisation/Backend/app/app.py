from flask import Flask
from flask_cors import CORS 
from .extensions import db 
from flask_sqlalchemy import SQLAlchemy
from .routes.register_routes import register_bp
from .routes.login_routes import login_bp
from .routes.home_routes import home_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    CORS(app)
    db.init_app(app)

    from .routes.conducteur import conducteur_bp
    from .routes.ride import ride_bp

    app.register_blueprint(conducteur_bp, url_prefix="/conducteur")
    app.register_blueprint(ride_bp, url_prefix="/ride")
    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(home_bp)

    with app.app_context():
        from .models.models import RideRequest, Conducteur
        db.create_all()

    return app
