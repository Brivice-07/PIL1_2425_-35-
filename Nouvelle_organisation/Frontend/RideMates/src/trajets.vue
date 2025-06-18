<template>
  <div class="trajets-container">
    <!-- En-tête (spécifique à cette page si non globalisé) -->
    <header class="header">
      <div class="header-content">
        <!-- Bouton de retour ajouté ici -->
        <button @click="goBack" class="back-button">
          <i class="fas fa-arrow-left"></i>
        </button>
        <div class="logo">
          <i class="fas fa-motorcycle"></i>
          <span>RideMates</span>
        </div>
      </div>
      <!-- Note: Si vous souhaitez une navbar globale comme celle d'Accueil,
           vous devriez créer un composant NavBar.vue et l'inclure ici ou dans App.vue. -->
    </header>
    
    <!-- Contenu principal -->
    <div class="container">
      <!-- Message d'information -->
      <div class="info-banner">
        <i class="fas fa-info-circle"></i>
        <div>Partagez votre trajet en moto ou en voiture. Notre plateforme est optimisée pour les motards mais accueille aussi les automobilistes.</div>
      </div>
      
      <!-- Onglets -->
      <div class="tabs">
        <div 
          class="tab" 
          :class="{ active: currentTab === 'passenger' }" 
          @click="selectTab('passenger')"
        >
          Passager
        </div>
        <div 
          class="tab" 
          :class="{ active: currentTab === 'driver' }" 
          @click="selectTab('driver')"
        >
          Conducteur
        </div>
      </div>
      
      <!-- Formulaire Passager -->
      <div class="form-container" v-if="currentTab === 'passenger'">
        <h2 class="form-title">
          <i class="fas fa-search"></i> Rechercher un trajet
        </h2>
        
        <!-- Sélection du type de véhicule pour passager -->
        <div class="vehicle-type">
          <div 
            class="vehicle-option moto" 
            :class="{ active: selectedPassengerVehicle === 'moto' }" 
            @click="selectPassengerVehicle('moto')"
          >
            <i class="fas fa-motorcycle"></i>
            <div>Trajet en moto</div>
          </div>
          <div 
            class="vehicle-option car" 
            :class="{ active: selectedPassengerVehicle === 'car' }" 
            @click="selectPassengerVehicle('car')"
          >
            <i class="fas fa-car"></i>
            <div>Trajet en voiture</div>
          </div>
        </div>
        
        <form @submit.prevent="searchTrips">
          <div class="form-row">
            <div class="form-col">
              <div class="form-group">
                <label for="passenger-departure">Départ</label>
                <input type="text" id="passenger-departure" v-model="passengerForm.departure" placeholder="Ville ou adresse de départ">
              </div>
            </div>
            
            <div class="form-col">
              <div class="form-group">
                <label for="passenger-arrival">Arrivée</label>
                <input type="text" id="passenger-arrival" v-model="passengerForm.arrival" placeholder="Ville ou adresse d'arrivée">
              </div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-col">
              <div class="form-group">
                <label for="passenger-date">Date</label>
                <input type="date" id="passenger-date" v-model="passengerForm.date">
              </div>
            </div>
            
            <div class="form-col">
              <div class="form-group">
                <label for="passengers">Nombre de passagers</label>
                <select id="passengers" v-model="passengerForm.passengers">
                  <option value="1">1 passager</option>
                  <option value="2">2 passagers</option>
                  <option value="3">3 passagers</option>
                  <option value="4">4 passagers</option>
                </select>
              </div>
            </div>
          </div>
          
          <button type="submit" class="btn btn-primary">
            <i class="fas fa-search btn-icon"></i> Rechercher des trajets
          </button>
        </form>
      </div>
      
      <!-- Résultats de recherche (cette section sera vide par défaut sans les exemples) -->
      <div class="results-container" v-if="currentTab === 'passenger'">
        <h2 class="form-title">
          <i class="fas fa-route"></i> Trajets disponibles
        </h2>
        
        <!-- Les exemples de trajets ont été retirés de cette section.
             Les résultats de recherche réels seraient affichés ici après une soumission de formulaire. -->
        <p v-if="true" style="text-align: center; color: #666; margin-top: 20px;">
          Aucun trajet trouvé pour le moment. Essayez une autre recherche !
        </p>
      </div>
      
      <!-- Formulaire Conducteur -->
      <div class="form-container" v-if="currentTab === 'driver'">
        <h2 class="form-title">
          <i class="fas fa-plus-circle"></i> Proposer un trajet
        </h2>
        
        <!-- Sélection du type de véhicule pour conducteur -->
        <div class="vehicle-type">
          <div 
            class="vehicle-option moto" 
            :class="{ active: selectedDriverVehicle === 'moto' }" 
            @click="selectDriverVehicle('moto')"
          >
            <i class="fas fa-motorcycle"></i>
            <div>Je propose un trajet en moto</div>
          </div>
          <div 
            class="vehicle-option car" 
            :class="{ active: selectedDriverVehicle === 'car' }" 
            @click="selectDriverVehicle('car')"
          >
            <i class="fas fa-car"></i>
            <div>Je propose un trajet en voiture</div>
          </div>
        </div>
        
        <form @submit.prevent="publishTrip">
          <div class="form-row">
            <div class="form-col">
              <div class="form-group">
                <label for="driver-departure">Départ</label>
                <input type="text" id="driver-departure" v-model="driverForm.departure" placeholder="Ville ou adresse de départ">
              </div>
            </div>
            
            <div class="form-col">
              <div class="form-group">
                <label for="driver-arrival">Arrivée</label>
                <input type="text" id="driver-arrival" v-model="driverForm.arrival" placeholder="Ville ou adresse d'arrivée">
              </div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-col">
              <div class="form-group">
                <label for="driver-date">Date</label>
                <input type="date" id="driver-date" v-model="driverForm.date">
              </div>
            </div>
            
            <div class="form-col">
              <div class="form-group">
                <label for="driver-time">Heure</label>
                <input type="time" id="driver-time" v-model="driverForm.time">
              </div>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-col">
              <div class="form-group">
                <label for="driver-seats">Places disponibles</label>
                <select id="driver-seats" v-model="driverForm.seats">
                  <option value="1">1 place</option>
                  <option value="2">2 places</option>
                  <option value="3">3 places</option>
                  <option value="4">4 places</option>
                </select>
              </div>
            </div>
            
            <div class="form-col">
              <div class="form-group">
                <label for="driver-price">Prix par passager (FCFA)</label>
                <input type="number" id="driver-price" v-model.number="driverForm.price" min="0">
              </div>
            </div>
          </div>
          
          <!-- Section véhicule dynamique (gérée par v-if / v-else) -->
          <div v-if="selectedDriverVehicle === 'moto'">
            <div class="form-group">
                <label for="driver-bike">Ma moto</label>
                <div class="form-row">
                    <div class="form-col">
                        <select id="driver-bike-brand" v-model="driverForm.vehicleDetails.brand">
                            <option value="">Marque de moto</option>
                            <option value="Honda">Honda</option>
                            <option value="Yamaha">Yamaha</option>
                            <option value="Kawasaki">Kawasaki</option>
                            <option value="Suzuki">Suzuki</option>
                            <option value="BMW">BMW</option>
                            <option value="Ducati">Ducati</option>
                            <option value="Triumph">Triumph</option>
                            <option value="Autre">Autre marque</option>
                        </select>
                    </div>
                    <div class="form-col">
                        <input type="text" id="driver-bike-model" v-model="driverForm.vehicleDetails.model" placeholder="Modèle de votre moto">
                    </div>
                </div>
            </div>
            
            <div class="form-group">
                <label for="driver-equipment">Équipement fourni</label>
                <div class="form-row">
                    <div class="form-col">
                        <select id="driver-equipment" v-model="driverForm.vehicleDetails.equipment">
                            <option value="casque">Casque fourni</option>
                            <option value="rien">Casque non fourni</option>
                        </select>
                    </div>
                </div>
            </div>
          </div>

          <div v-else-if="selectedDriverVehicle === 'car'">
            <div class="form-group">
                <label for="driver-car">Ma voiture</label>
                <div class="form-row">
                    <div class="form-col">
                        <select id="driver-car-brand" v-model="driverForm.vehicleDetails.brand">
                            <option value="">Marque de voiture</option>
                            <option value="Peugeot">Peugeot</option>
                            <option value="Renault">Renault</option>
                            <option value="Citroën">Citroën</option>
                            <option value="Volkswagen">Volkswagen</option>
                            <option value="BMW">BMW</option>
                            <option value="Mercedes">Mercedes</option>
                            <option value="Audi">Audi</option>
                            <option value="Autre">Autre marque</option>
                        </select>
                    </div>
                    <div class="form-col">
                        <input type="text" id="driver-car-model" v-model="driverForm.vehicleDetails.model" placeholder="Modèle de votre voiture">
                    </div>
                </div>
            </div>
            

          </div>
          
          <div class="form-group">
            <label for="driver-description">Description du trajet</label>
            <textarea id="driver-description" v-model="driverForm.description" placeholder="Informations sur votre véhicule, style de conduite, arrêts prévus, etc."></textarea>
          </div>
          
          <button type="submit" class="btn btn-primary">
            <i class="fas fa-paper-plane btn-icon"></i> Publier ce trajet
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Trajets",
  data() {
    return {
      currentTab: 'passenger', // Onglet actif : 'passenger' (passager) ou 'driver' (conducteur)
      selectedPassengerVehicle: 'moto', // Type de véhicule sélectionné par le passager : 'moto' ou 'car'
      selectedDriverVehicle: 'moto', // Type de véhicule sélectionné par le conducteur : 'moto' ou 'car'

      // Données du formulaire pour la recherche de trajets (passager)
      passengerForm: {
        departure: '',
        arrival: '',
        date: '',
        passengers: '1' // Nombre de passagers par défaut
      },
      // Données du formulaire pour la proposition de trajet (conducteur)
      driverForm: {
        departure: '',
        arrival: '',
        date: '',
        time: '',
        seats: '1', // Places disponibles par défaut
        price: 15, // Prix par passager par défaut
        vehicleDetails: { // Détails du véhicule, dynamiques selon le type (moto/voiture)
          brand: '',
          model: '',
          equipment: 'casque', // Spécifique à la moto
        },
        description: ''
      }
    };
  },
  methods: {
     // Méthode pour naviguer vers la page précédente (ou la page d'accueil si aucune historique)
    goBack() {
        // Si l'historique du navigateur le permet, revenir en arrière
        if (window.history.length > 1) {
          this.$router.go(-1);
        } else {
          // Sinon, naviguer explicitement vers la page d'accueil
          this.$router.push('/'); // Assurez-vous que '/' est la route de votre page Accueil.vue
        }
    },
    // Méthode pour changer l'onglet actif (Passager/Conducteur)
    selectTab(tab) {
      this.currentTab = tab;
      // Réinitialise la sélection de véhicule par défaut lors du changement d'onglet
      if (tab === 'passenger') {
        this.selectedPassengerVehicle = 'moto';
      } else {
        this.selectedDriverVehicle = 'moto';
      }
    },
    // Méthode pour sélectionner le type de véhicule pour la recherche (Passager)
    selectPassengerVehicle(type) {
      this.selectedPassengerVehicle = type;
    },
    // Méthode pour sélectionner le type de véhicule pour la proposition (Conducteur)
    selectDriverVehicle(type) {
      this.selectedDriverVehicle = type;
      // Réinitialise les détails du véhicule quand le type change
      this.driverForm.vehicleDetails = {
        brand: '',
        model: '',
        equipment: type === 'moto' ? 'casque' : 'standard', // Définit l'équipement par défaut pour moto
        color: '', // Vide pour la voiture
        comfort: 'standard' // Définit le confort par default pour la voiture
      };
    },
    // Méthode pour définir les valeurs initiales des champs de date et heure
    setInitialFormValues() {
      // Date du jour par défaut
      const today = new Date().toISOString().split('T')[0];
      this.passengerForm.date = today;
      this.driverForm.date = today;

      // Heure actuelle + 1h par défaut
      const now = new Date();
      now.setHours(now.getHours() + 1);
      this.driverForm.time = now.toTimeString().substring(0, 5);
    },
    // Méthode de soumission du formulaire de recherche de trajets (Passager)
    searchTrips() {
      console.log("Recherche de trajets :", this.passengerForm, "Véhicule :", this.selectedPassengerVehicle);
      // Ici, vous ajouteriez la logique réelle pour interroger une API et afficher les résultats.
      alert("Recherche de trajets en cours (voir console pour les données) !");
    },
    // Méthode de soumission du formulaire de proposition de trajet (Conducteur)
    publishTrip() {
      console.log("Publication de trajet :", this.driverForm, "Véhicule :", this.selectedDriverVehicle);
      // Ici, vous ajouteriez la logique réelle pour envoyer les données à une API backend.
      alert("Votre trajet a été publié avec succès (voir console pour les données) !");
    }
  },
  mounted() {
    // Appelle cette méthode une fois que le composant est monté pour initialiser les champs
    this.setInitialFormValues();
  }
};
</script>

<style scoped>
/* Variables CSS spécifiques à ce composant (RETIRÉES DE :ROOT) */
/* Les variables primaires et d'autres comme light, dark, etc. sont maintenant globales dans App.vue */
/* Les couleurs spécifiques à cette page sont utilisées directement ou définies localement si réutilisées. */
/* Les variables suivantes sont spécifiques à ce composant et peuvent être utilisées directement ou comme des custom properties ici. */
/* Nous utiliserons des valeurs hexadécimales directes pour simplifier et éviter les conflits de nommage avec les variables globales. */

/* Styles généraux pour le composant */
.trajets-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Header */
.header {
    background-color: var(--primary); /* Utilise la variable globale */
    color: white;
    padding: 15px 20px;
    display: flex;
    justify-content: center; /* Centré pour cette page */
    align-items: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center; /* Centrer le contenu du header */
  width: 100%;
}

.logo {
    font-size: 24px;
    font-weight: bold;
    display: flex;
    align-items: center;
}

.logo i {
    margin-right: 10px;
    color: white; /* Couleur orange directe pour l'icône de moto spécifique à cette page */
}

  /* Styles pour le bouton de retour */
.back-button {
  position: absolute; /* Positionne le bouton par rapport au header */
  left: 20px; /* Aligné à gauche */
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: background-color 0.2s ease-in-out;
  display: flex; /* Pour centrer l'icône */
  align-items: center;
  justify-content: center;
}

.back-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Contenu principal */
.container {
    max-width: 1200px;
    margin: 20px auto;
    padding: 0 20px;
    flex: 1; /* Permet au contenu de prendre l'espace disponible */
}

/* Message d'information */
.info-banner {
    background-color: #f0f7f5;
    border-left: 4px solid var(--primary); /* Utilise la variable globale */
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 0 5px 5px 0;
    display: flex;
    align-items: center;
}

.info-banner i {
    color: var(--primary); /* Utilise la variable globale */
    margin-right: 10px;
    font-size: 20px;
}

/* Onglets */
.tabs {
    display: flex;
    margin-bottom: 20px;
    border-bottom: 1px solid #ddd;
}

.tab {
    padding: 12px 25px;
    cursor: pointer;
    font-weight: bold;
    color: #666;
    border-bottom: 3px solid transparent;
    transition: all 0.2s;
}

.tab.active {
    color: var(--primary); /* Utilise la variable globale */
    border-bottom-color: var(--primary); /* Utilise la variable globale */
}

/* Type de véhicule */
.vehicle-type {
    display: flex;
    margin-bottom: 20px;
    gap: 15px;
}

.vehicle-option {
    flex: 1;
    padding: 15px;
    border: 2px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    text-align: center;
    transition: all 0.2s;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.vehicle-option i {
    font-size: 24px;
    margin-bottom: 10px;
}

.vehicle-option.active {
    border-color: var(--primary); /* Utilise la variable globale */
    background-color: #f0f7f5;
}

.vehicle-option.moto.active {
    border-color: #E67E22; /* Couleur orange directe */
    background-color: #fef5ee;
}

.vehicle-option.car.active {
    border-color: #3498db; /* Couleur bleue directe */
    background-color: #f0f7fc;
}

.vehicle-option.moto i {
    color: #E67E22; /* Couleur orange directe */
}

.vehicle-option.car i {
    color: #3498db; /* Couleur bleue directe */
}

/* Formulaires */
.form-container {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    padding: 30px;
    margin-bottom: 30px;
}

.form-title {
    font-size: 20px;
    margin-bottom: 25px;
    color: var(--primary); /* Utilise la variable globale */
    display: flex;
    align-items: center;
}

.form-title i {
    margin-right: 10px;
}

.form-group {
    /* Anciennement 20px, augmenté pour plus d'espace */
    margin-bottom: 25px; /* Augmenté à 25px pour plus d'espace */
}

.form-row {
    display: flex;
    gap: 50px;
    /* margin-bottom: 20px;  Ce margin-bottom est déjà couvert par le form-group du dessous */
}

/* Note: Le .form-group à l'intérieur de .form-row gère maintenant l'espacement vertical */

.form-col {
    flex: 1;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
}

input, select, textarea {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
    transition: border 0.3s;
}

input:focus, select:focus, textarea:focus {
    border-color: var(--primary); /* Utilise la variable globale */
    outline: none;
}

textarea {
    min-height: 100px;
    resize: vertical;
}

/* Boutons */
.btn {
    padding: 12px 25px;
    border-radius: 5px;
    font-weight: bold;
    cursor: pointer;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    font-size: 16px;
}

.btn-primary {
    background-color: var(--primary); /* Utilise la variable globale */
    color: white;
}

.btn-primary:hover {
    background-color: #0c4b3f; /* Utilise une valeur directe pour le hover */
}

.btn-icon {
    margin-right: 8px;
}

/* Résultats de recherche */
.results-container {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    padding: 20px;
}

.ride-card {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    transition: transform 0.2s;
    position: relative;
}

.ride-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.ride-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
    color: white;
}

.ride-badge.moto {
    background-color: #E67E22; /* Couleur orange directe */
}

.ride-badge.car {
    background-color: #3498db; /* Couleur bleue directe */
}

.ride-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
    padding-right: 80px;
}

.ride-title {
    font-size: 18px;
    font-weight: bold;
    color: var(--primary); /* Utilise la variable globale */
}

.ride-price {
    background-color: var(--primary); /* Utilise la variable globale */
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
}

.route {
    display: flex; /* Cela doit être la route elle-même */
    flex-direction: column; /* Les points s'affichent en colonne */
    margin-bottom: 15px;
}

.point {
    display: flex;
    margin-bottom: 10px;
    align-items: center; /* Aligner icône et texte verticalement */
}

.point-icon {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background-color: var(--primary); /* Utilise la variable globale */
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    flex-shrink: 0;
    font-size: 12px;
}

.point-destination .point-icon {
    background-color: #E67E22; /* Couleur orange directe */
}

.point-content {
    flex: 1;
}

.point-title {
    font-weight: bold;
    margin-bottom: 2px;
}

.point-address {
    color: #666;
    font-size: 14px;
}

.point-time {
    font-size: 14px;
    color: var(--primary); /* Utilise la variable globale */
    font-weight: bold;
}

.ride-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #eee;
}

.driver-info {
    display: flex;
    align-items: center;
}

.driver-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: var(--primary); /* Utilise la variable globale */
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    font-size: 16px;
}

.driver-name {
    font-weight: bold;
}

.driver-vehicle {
    font-size: 14px;
    color: #666;
}

.btn-sm {
    padding: 8px 15px;
    font-size: 14px;
}

/* Responsive */
@media (max-width: 768px) {
    .form-row {
        flex-direction: column;
        gap: 0; 
    }
    
    .vehicle-type {
        flex-direction: column;
    }
    
    .ride-header, .ride-footer {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }
    
    .ride-header {
        padding-right: 0;
    }

    /* Ajustements pour les points de route sur mobile */
    .route .point {
      margin-bottom: 15px;
    }
    .route .point:last-child {
      margin-bottom: 0;
    }
}
</style>
