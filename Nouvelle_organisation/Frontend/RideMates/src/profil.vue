<template>
  <div class="profil-page-wrapper">
    <!-- En-tête de la page profil -->
    <header class="profil-header">
      <button @click="goBack" class="back-button">
        <i class="fas fa-arrow-left"></i>
      </button>
      <h2 class="titre">
        <i class="fas fa-user-circle profile-icon"></i> Mon Profil
      </h2>
    </header>

    <div class="main-content-wrapper">
      <section class="profil-container">
        <!-- Formulaire de profil -->
        <form @submit.prevent="handleSubmit" class="formulaire">
          <div class="grid">
            <!-- Nom -->
            <div class="ligne">
              <label for="lastName">Nom</label>
              <input id="lastName" v-model="profile.lastName" type="text" required />
            </div>
            <!-- Prénom -->
            <div class="ligne">
              <label for="firstName">Prénom</label>
              <input id="firstName" v-model="profile.firstName" type="text" required />
            </div>
          </div>

          <!-- Email -->
          <div class="ligne">
            <label for="email">Email</label>
            <input id="email" v-model="profile.email" type="email" required />
          </div>

          <!-- Téléphone -->
          <div class="ligne">
            <label for="phone">Téléphone</label>
            <input id="phone" v-model="profile.phone" type="tel" required />
          </div>

          <!-- Rôle -->
          <div class="ligne">
            <label for="role">Rôle</label>
            <select id="role" v-model="profile.role" class="select-styled">
              <option value="conducteur">Conducteur</option>
              <option value="passager">Passager</option>
            </select>
          </div>

          <!-- Informations véhicule (si conducteur) -->
          <div v-if="profile.role === 'conducteur'" class="vehicule">
            <h3>Informations du véhicule</h3>

            <div class="ligne">
              <label for="vehicle-type-select">Type de véhicule</label>
              <select id="vehicle-type-select" v-model="profile.vehicle.type" class="select-styled">
                <option value="moto">Moto</option>
                <option value="car">Voiture</option>
              </select>
            </div>

            <div class="grid">
              <div class="ligne">
                <label for="vehicle-make">Marque</label>
                <select id="vehicle-make" v-model="profile.vehicle.make" class="select-styled">
                  <option value="">Sélectionnez une marque</option>
                  <template v-if="profile.vehicle.type === 'moto'">
                    <option v-for="brand in motoBrands" :key="brand" :value="brand">{{ brand }}</option>
                  </template>
                  <template v-else-if="profile.vehicle.type === 'car'">
                    <option v-for="brand in carBrands" :key="brand" :value="brand">{{ brand }}</option>
                  </template>
                </select>
              </div>
              <div class="ligne">
                <label for="vehicle-model">Modèle</label>
                <input id="vehicle-model" v-model="profile.vehicle.model" type="text" placeholder="Saisissez le modèle" />
              </div>
            </div>
            <div class="ligne">
              <label for="vehicle-seats">Nombre de places disponibles</label>
              <input id="vehicle-seats" v-model.number="profile.vehicle.seats" type="number" min="1" max="10" />
            </div>
          </div>

          <!-- Bouton d'enregistrement-->
          <button type="submit" class="bouton">
            <i class="fas fa-save bouton-icon"></i> Enregistrer les modifications
          </button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const profile = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  role: 'passager',
  vehicle: {
    type: 'moto',
    make: '',
    model: '',
    seats: 1
  }
})

const motoBrands = [
  'Honda', 'Yamaha', 'Kawasaki', 'Suzuki', 'BMW', 'Ducati', 'Triumph', 'Harley-Davidson', 'KTM', 'Aprilia', 'Autre'
]
const carBrands = [
  'Peugeot', 'Renault', 'Citroën', 'Volkswagen', 'BMW', 'Mercedes', 'Audi', 'Toyota', 'Ford', 'Tesla', 'Autre'
]

watch(() => profile.value.vehicle.type, () => {
  profile.value.vehicle.make = ''
  profile.value.vehicle.model = ''
})

watch(() => profile.value.vehicle.make, () => {
  profile.value.vehicle.model = ''
})

function goBack() {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}

function handleSubmit() {
  console.log('Profil mis à jour:', profile.value)
  alert('Profil mis à jour avec succès ! (Voir console)')
}

// Charger les données depuis l'API
onMounted(async () => {
  const token = localStorage.getItem("token")
  if (!token) {
    alert("Aucun token trouvé. Veuillez vous reconnecter.")
    return
  }

  try {
    const res = await fetch('http://localhost:5000/api/home', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    const data = await res.json()
    console.log("Données reçues :", data)

    if (data.utilisateur) {
      profile.value.firstName = data.utilisateur.firstName || ''
      profile.value.lastName = data.utilisateur.lastName || ''
      profile.value.email = data.utilisateur.email || ''
      profile.value.phone = data.utilisateur.phone || ''
      profile.value.role = data.utilisateur.role || 'passager'

      // Ajoute ceci si tu veux aussi charger les infos véhicule si elles existent :
      if (data.utilisateur.vehicle) {
        profile.value.vehicle = {
          type: data.utilisateur.vehicle.type || 'moto',
          make: data.utilisateur.vehicle.make || '',
          model: data.utilisateur.vehicle.model || '',
          seats: data.utilisateur.vehicle.seats || 1
        }
      }
    }
  } catch (err) {
    console.error("Erreur lors du chargement du profil :", err)
  }
})
</script>



<style scoped>
  /* Les variables globales sont maintenant définies dans App.vue.
    Nous utilisons ici les variables globales ou des valeurs directes. */

  /* Conteneur principal de la page pour une meilleure mise en page */
  .profil-page-wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    background-color: #f5f5f5; /* Un fond clair pour toute la page */
  }

  /* En-tête de la page profil */
  .profil-header {
    background-color: var(--primary); /* Couleur principale de l'application */
    color: white;
    padding: 15px 20px;
    display: flex;
    align-items: center;
    justify-content: center; /* Centre le titre */
    position: relative; /* Pour positionner le bouton de retour */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }

  .titre {
    font-size: 2.5rem; /* Taille de police légèrement réduite pour l'en-tête */
    font-weight: bold;
    text-align: center;
    margin: 0; /* Supprime la marge par défaut */
    flex-grow: 1; /* Permet au titre de prendre l'espace restant pour le centrer */
    display: flex; /* Permet l'alignement de l'icône et du texte */
    align-items: center; /* Aligne verticalement */
    justify-content: center; /* Centre le contenu (icône + texte) */
  }

  .profile-icon {
    margin-right: 10px; /* Espace entre l'icône et le texte */
    font-size: 1.1em; /* Ajuste la taille de l'icône par rapport au texte */
  }

  /* Styles pour le bouton de retour (similaire aux autres pages) */
  .back-button {
    position: absolute;
    left: 20px;
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
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .back-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .main-content-wrapper {
    flex: 1; /* Permet au contenu de prendre l'espace disponible */
    display: flex;
    justify-content: center; /* Centre horizontalement */
    align-items: flex-start; /* Aligne en haut */
    padding: 20px;
  }

  .profil-container {
    max-width: 700px; /* Largeur maximale pour le formulaire */
    width: 100%; /* Prend toute la largeur disponible jusqu'à max-width */
    background-color: var(--primary); /* Utilise la variable globale pour le fond */
    border-radius: 15px; /* Coins arrondis pour un aspect doux */
    box-shadow: 0 5px 20px rgba(0,0,0,0.1); /* Ombre plus prononcée pour la profondeur */
    padding: 2.5rem; /* Plus de padding interne */
    color: white; /* Couleur du texte par défaut à l'intérieur */
    margin: 20px auto; /* Centré horizontalement et espace vertical */
  }

  .formulaire {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .ligne {
    display: flex;
    flex-direction: column;
    gap: 0.6rem; /* Ajusté légèrement l'espace */
  }

  .ligne label {
    font-weight: 600; /* Un peu plus de poids */
    color: rgba(255, 255, 255, 0.9); /* Un blanc légèrement transparent pour le label */
    font-size: 1.05rem; /* Légèrement plus grand */
  }

  input,
  .select-styled { /* Applique les styles aux selects */
    padding: 0.85rem; /* Augmenté pour un meilleur toucher */
    border: 1px solid white; /* Bordure blanche OPAQUE pour une meilleure visibilité */
    border-radius: 0.5rem; /* Plus arrondis */
    font-size: 1rem;
    background-color: white; /* Fond blanc OPAQUE */
    color: var(--primary); /* Texte en couleur primaire pour le contraste */
    transition: all 0.3s ease; /* Transition douce pour les changements de style */
  }

  input:focus,
  .select-styled:focus {
    border: 2px solid white; /* Bordure plus épaisse et OPAQUE au focus */
    outline: none;
    box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.4); /* Ombre plus visible au focus */
    background-color: white; /* Fond blanc OPAQUE au focus */
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); /* Min-width légèrement augmenté */
    gap: 1.5rem;
  }

  .vehicule {
    background-color: rgba(255, 255, 255, 0.08); /* Fond très légèrement transparent */
    padding: 1.8rem; /* Plus de padding */
    border-radius: 0.8rem; /* Plus arrondis */
    margin-top: 2rem; /* Plus de marge au-dessus */
    color: white; /* Texte blanc à l'intérieur */
    border: 1px solid rgba(255, 255, 255, 0.1); /* Bordure très subtile */
    box-shadow: 0 2px 10px rgba(0,0,0,0.15); /* Ombre douce */
  }

  .vehicule h3 {
    margin-top: 0;
    margin-bottom: 1rem;
    font-size: 1.4rem; /* Taille de police légèrement plus grande */
    border-bottom: 1px solid rgba(255, 255, 255, 0.3); /* Ligne de séparation blanche transparente */
    padding-bottom: 0.8rem; /* Plus de padding sous la ligne */
    color: rgba(255, 255, 255, 0.95); /* Couleur plus marquée pour le titre */
  }

  .bouton {
    background-color: white; /* Bouton principal blanc */
    color: var(--primary); /* Texte du bouton en couleur primaire */
    padding: 18px 30px; /* Padding généreux */
    border: none;
    border-radius: 0.75rem; /* Très arrondis */
    cursor: pointer;
    align-self: center;
    transition: all 0.3s ease; /* Transition pour tous les changements de style */
    margin-top: 2rem; /* Plus d'espace au-dessus du bouton */
    font-size: 1.15rem; /* Taille de police légèrement plus grande */
    font-weight: bold;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2); /* Ombre prononcée */
    display: flex;
    align-items: center;
    gap: 10px; /* Espace entre l'icône et le texte */
  }

  .bouton-icon {
    font-size: 1.3em; /* Taille de l'icône */
  }

  .bouton:hover {
    background-color: var(--secondary); /* Nouvelle couleur au survol, par exemple un vert plus clair */
    color: white; /* Texte blanc au survol */
    transform: translateY(-3px); /* Effet de soulèvement plus prononcé */
    box-shadow: 0 6px 20px rgba(0,0,0,0.3); /* Ombre plus prononcée au survol */
  }


  /* Responsive pour les petits écrans */
  @media (max-width: 768px) {
    .profil-header .titre {
      font-size: 2rem;
    }
    .back-button {
      left: 15px;
      font-size: 20px;
    }
    .main-content-wrapper {
      padding: 15px;
    }
    .profil-container {
      padding: 2rem; /* Un peu moins de padding sur les écrans plus petits */
      border-radius: 10px; /* Coins un peu moins arrondis sur mobile */
    }
    .grid {
      grid-template-columns: 1fr; /* Une seule colonne sur mobile */
      gap: 1rem;
    }
    .formulaire {
      gap: 1rem;
    }
    .bouton {
      width: 100%; /* Bouton prend toute la largeur sur mobile */
      align-self: stretch; /* S'étire */
      padding: 15px 20px;
      font-size: 1rem;
      margin-top: 1.5rem;
    }
    .vehicule {
      padding: 1.5rem;
      margin-top: 1.5rem;
    }
    .vehicule h3 {
      font-size: 1.2rem;
      padding-bottom: 0.5rem;
    }
  }

  @media (max-width: 480px) {
    .profil-header .titre {
      font-size: 1.8rem;
    }
    .profil-container {
      padding: 1.5rem;
    }
    .ligne label {
      font-size: 0.95rem;
    }
    input, .select-styled {
      padding: 0.75rem;
      font-size: 0.9rem;
    }
    .vehicule {
      padding: 1rem;
    }
    .bouton {
      padding: 12px 18px;
      font-size: 0.95rem;
    }
  }
</style>