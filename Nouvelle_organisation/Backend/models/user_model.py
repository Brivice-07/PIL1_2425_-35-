from app import db

class Utilisateur(db.Model):
    _tablename_ = "utilisateurs"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=True)
    prenoms = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telephone = db.Column(db.String(20), unique=True, nullable=True)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    statut = db.Column(db.Enum('conducteur', 'passager', name='statut_enum'), nullable=False)
    profil = db.Column(db.String(255), nullable=True)
    point_de_depart = db.Column(db.String(255), nullable=True)
    horaires = db.Column(db.String(255), nullable=True)

    def _repr_(self):
        return f"<Utilisateur {self.prenoms} {self.nom} - {self.email}>"