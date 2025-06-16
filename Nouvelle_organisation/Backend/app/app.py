from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    from .conducteur.routes import conducteur_bp
    from .ride.routes import ride_bp

    app.register_blueprint(conducteur_bp, url_prefix="/conducteur")
    app.register_blueprint(ride_bp, url_prefix="/ride")

    with app.app_context():
        from .models import RideRequest, Conducteur
        db.create_all()

    return app
