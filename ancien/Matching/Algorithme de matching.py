from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import openrouteservice
#Initialisation de Flask
app = Flask("WayX")
#Ajouter la clé OpenRouteService
client = openrouteservice.Client(key='5b3ce3597851110001cf624830dd089e936245beaae668bc47a6b315')
#Connexion à la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Brivice@localhost:3306/Ifri_comotorage'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Conducteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    places_disponibles = db.Column(db.Integer, nullable=False)
    distance_max_detour = db.Column(db.Float, default=5.0)
try:
    with app.app_context():
        db.create_all()
        print("✅Base de données initialisée avec succès!")
except Exception as e:
    print("❌Erreur MySQL :", e)
@app.route('/ajouter_conducteur', methods=["POST"])
#Fonction pour ajouter un conducteur
def ajouter_conducteur():
    data = request.json
    existe = Conducteur.query.filter_by(latitude=data.get('latitude'), longitude=data.get('longitude')).first()
    if existe:
        return jsonify({"error": "Conducteur déjà enregistré"}), 400  
    if not all(k in data for k in ["latitude", "longitude", "places"]):
        return jsonify({"error": "Données incomplètes. Veuillez fournir latitude, longitude et places"}), 400
    try:
        nouveau_conducteur = Conducteur(
            latitude=float(data.get('latitude')),
            longitude=float(data.get('longitude')),
            places_disponibles=int(data.get('places'))
    )
        db.session.add(nouveau_conducteur)
        db.session.commit()
        return jsonify({"message": "✅Conducteur ajouté avec succès!"})
    except Exception as e:
        print("❌Erreur d'insertion MySQL :", e)
        return jsonify({"error": "Erreur lors de l'ajout du conducteur"}), 500
#Coordonnées IFRI
IFRI_COORD = [2.4245, 6.3624]
#Recherche des conducteurs disponibles
@app.route('/conducteurs', methods=['GET'])
def voir_conducteur():
    conducteurs = Conducteur.query.all()
    return jsonify([
       { 
           "id": c.id,
        "depart":(c.latitude, c.longitude),
        "places_disponibles": c.places_disponibles
       }
       for c in conducteurs
    ])
#Fonction pour obtenir la distance et la durée
def get_distance_km_duree_min(start, via, end):
    try:
        result = client.directions(coordinates=[start, via, end], profile='driving-car', format='geojson')
        segment_start_via = result['routes'][0]['segments'][0]
        segment_via_end = result['routes'][0]['segments'][1]
        distance = (segment_start_via ['distance'] + segment_via_end['distance'])/1000
        duration = (segment_start_via ['duration'] + segment_via_end['duration'])/60
        return distance, duration
    except Exception as e:
        print("Erreur ORS:", e)
        return float('inf'), float('inf')
#Endpoint Flask pour le matching  
@app.route('/match', methods=["POST"])
def match_passager():
    data = request.json
    if not data or "depart" not in data:
        return jsonify({"error": "Données invalides. Veuillez entrer un point de départ"}), 400
    try:
        depart_passager = tuple(data.get('depart'))
    except TypeError:
        return jsonify({"error": "Format du point de départ invalide"}), 400
    conducteurs=Conducteur.query.all()
    matches = []
    for conducteur in conducteurs:
        if conducteur.places_disponibles == 0:
             continue
        #Comparer les distances entre les passagers→conducteur→IFRI
        distance_depart,_=get_distance_km_duree_min(depart_passager, (conducteur.latitude, conducteur.longitude))
        distance_arrivee,_=get_distance_km_duree_min((conducteur.latitude, conducteur.longitude), IFRI_COORD)
        #Accepter si le detour est raisonnable(<5km par exemple)
        if distance_depart <= 5:
            matches.append({
                "conducteur_id": conducteur.id,
                "nom": conducteur.nom,
                "photo": conducteur.profil,
                "distance_detour": round(distance_depart, 2),
                "distance_totale": round(distance_arrivee + distance_depart, 2),
                "itinéraire": f"{depart_passager}→{IFRI_COORD}",
                "heure_depart": conducteur.heure_depart,
                "places_disponibles": conducteur.places_disponibles
            })
    return jsonify(matches)
    matches.sort(key=lambda x: x["distance_detour"])
#Lancer l'application Flask
if __name__=='_main_':
    app.run(debug=True)

