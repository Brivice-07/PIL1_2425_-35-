from app.covoiturage.models import Offer, Request
from geopy.distance import geodesic # Nécessite 'geopy'
from datetime import datetime, timedelta

def find_matches(offer: Offer, radius_km: float = 5, time_tolerance_minutes: int = 30):
    """
    Trouve les demandes de trajet (requests) qui correspondent à une offre donnée.

    :param offer: L'objet Offer à matcher.
    :param radius_km: Le rayon en km pour la correspondance géographique.
    :param time_tolerance_minutes: La tolérance en minutes pour la correspondance horaire.
    :return: Une liste d'objets Request correspondants.
    """
    if not offer.start_latitude or not offer.start_longitude or \
       not offer.end_latitude or not offer.end_longitude:
        # Ne peut pas matcher géographiquement sans coordonnées
        return []

    # Filtrer les demandes en attente
    potential_requests = Request.query.filter_by(status='pending').all()
    matches = []

    offer_start_coords = (offer.start_latitude, offer.start_longitude)
    offer_end_coords = (offer.end_latitude, offer.end_longitude)

    for req in potential_requests:
        if not req.start_latitude or not req.start_longitude or \
           not req.end_latitude or not req.end_longitude:
            continue # Passer si les coordonnées de la demande sont manquantes

        req_start_coords = (req.start_latitude, req.start_longitude)
        req_end_coords = (req.end_latitude, req.end_longitude)

        # 1. Correspondance Géographique (point de départ et d'arrivée)
        # Calculer la distance entre les points de départ
        dist_start = geodesic(offer_start_coords, req_start_coords).km
        # Calculer la distance entre les points d'arrivée
        dist_end = geodesic(offer_end_coords, req_end_coords).km

        if dist_start <= radius_km and dist_end <= radius_km:
            # 2. Correspondance Horaire
            # La demande doit vouloir partir autour de l'heure de départ de l'offre
            # Et arriver avant ou autour de l'heure d'arrivée estimée de l'offre
            time_diff_departure = abs((offer.departure_time - req.desired_departure_time).total_seconds() / 60)

            # Vérifier si l'heure de départ de la demande est dans la tolérance de l'offre
            if time_diff_departure <= time_tolerance_minutes:
                # Vérifier si l'heure d'arrivée souhaitée par le passager est compatible
                # (ex: pas plus tard que l'arrivée estimée du conducteur + une marge)
                if req.desired_arrival_time_latest and offer.arrival_time_estimate:
                    if req.desired_arrival_time_latest <= offer.arrival_time_estimate + timedelta(minutes=time_tolerance_minutes):
                        matches.append(req)
                elif not req.desired_arrival_time_latest: # Si le passager n'a pas d'heure limite
                    matches.append(req)
                # Note: Vous pourriez ajouter une logique pour les jours récurrents ici

    return matches

# Vous pouvez ajouter une fonction similaire pour trouver les offres correspondant à une demande
def find_offers_for_request(request: Request, radius_km: float = 5, time_tolerance_minutes: int = 30):
    """
    Trouve les offres de trajet (offers) qui correspondent à une demande donnée.
    Implémentation similaire à find_matches mais inversée.
    """
    # Implémentation similaire à find_matches, mais on filtre Offers et on compare avec Request
    if not request.start_latitude or not request.start_longitude or \
       not request.end_latitude or not request.end_longitude:
        return []

    potential_offers = Offer.query.filter_by(status='pending').all()
    matches = []

    req_start_coords = (request.start_latitude, request.start_longitude)
    req_end_coords = (request.end_latitude, request.end_longitude)

    for offer in potential_offers:
        if not offer.start_latitude or not offer.start_longitude or \
           not offer.end_latitude or not offer.end_longitude:
            continue

        offer_start_coords = (offer.start_latitude, offer.start_longitude)
        offer_end_coords = (offer.end_latitude, offer.end_longitude)

        dist_start = geodesic(offer_start_coords, req_start_coords).km
        dist_end = geodesic(offer_end_coords, req_end_coords).km

        if dist_start <= radius_km and dist_end <= radius_km:
            time_diff_departure = abs((offer.departure_time - request.desired_departure_time).total_seconds() / 60)

            if time_diff_departure <= time_tolerance_minutes:
                if request.desired_arrival_time_latest and offer.arrival_time_estimate:
                    if request.desired_arrival_time_latest <= offer.arrival_time_estimate + timedelta(minutes=time_tolerance_minutes):
                        matches.append(offer)
                elif not request.desired_arrival_time_latest:
                    matches.append(offer)
    return matches