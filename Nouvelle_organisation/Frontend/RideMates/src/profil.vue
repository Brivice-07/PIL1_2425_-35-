<template>
  <h2 class="titre"> Mon Profil</h2>
  <div class="utile">
    <section class="profil-container">
      <!-- Formulaire -->
      <form @submit.prevent="handleSubmit" class="formulaire">
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
          <select id="role" v-model="profile.role">
            <option value="conducteur">Conducteur</option>
            <option value="passager">Passager</option>
          </select>
        </div>

        <!-- Informations véhicule (si conducteur) -->
        <div v-if="profile.role === 'conducteur'" class="vehicule">
          <h3>Informations du véhicule</h3>
          
          <div class="ligne">
            <label for="vehicle-type-select">Type de véhicule</label>
            <select id="vehicle-type-select" v-model="profile.vehicle.type">
              <option value="moto">Moto</option>
              <option value="car">Voiture</option>
            </select>
          </div>

          <div class="grid">
            <div class="ligne">
              <label for="vehicle-make">Marque</label>
              <select id="vehicle-make" v-model="profile.vehicle.make">
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
        <button type="submit" class="bouton">Enregistrer les modifications</button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const profile = ref({
  firstName: '', // Prénom séparé
  lastName: '',  // Nom séparé
  email: '',
  phone: '',
  role: 'passager', // Rôle par défaut, pour commencer
  vehicle: {
    type: 'moto', // Type de véhicule par défaut
    make: '',    // Marque sélectionnée
    model: '',   // Modèle saisi manuellement
    seats: 1     // Nombre de places par défaut
  }
})

// Listes des marques (les modèles seront saisis manuellement)
const motoBrands = [
  'Honda', 'Yamaha', 'Kawasaki', 'Suzuki', 'BMW', 'Ducati', 'Triumph', 'Harley-Davidson', 'KTM', 'Aprilia', 'Autre'
];
const carBrands = [
  'Peugeot', 'Renault', 'Citroën', 'Volkswagen', 'BMW', 'Mercedes', 'Audi', 'Toyota', 'Ford', 'Tesla', 'Autre'
];

// Supprimez la propriété calculée 'availableModels' car le modèle est maintenant un input text.
// Supprimez les objets 'motoModelsByBrand' et 'carModelsByBrand' car les modèles sont saisis manuellement.

// Surveille les changements de type de véhicule et de marque pour réinitialiser la marque et le modèle
watch(() => profile.value.vehicle.type, () => {
  profile.value.vehicle.make = '';  // Réinitialise la marque quand le type change
  profile.value.vehicle.model = ''; // Réinitialise le modèle quand le type change
});

watch(() => profile.value.vehicle.make, () => {
  profile.value.vehicle.model = ''; // Réinitialise le modèle quand la marque change
});

function handleSubmit() {
  console.log('Profil mis à jour:', profile.value)
  // Ici, vous ajouteriez la logique pour sauvegarder les données, par exemple vers une API
  alert('Profil mis à jour avec succès ! (Voir console)');
}
</script>

<style scoped>
/* Les variables globales sont maintenant définies dans App.vue.
   Nous utilisons ici les variables globales ou des valeurs directes. */

.profil-container {
  max-width: 800px;
  margin: auto;
  padding: 2rem;
}

.titre {
  font-size: 3rem;
  font-weight: 900; /* Le poids de la police est souvent 100-900, pas 90px */
  text-align: center;
  margin-bottom: 1.5rem;
  /* margin-right: 20px;  Souvent pas nécessaire pour un titre centré dans un conteneur */
}

.formulaire {
  display: flex;
  flex-direction: column;
  gap: 1.5rem; /* Augmenté à 1.5rem pour plus d'espace entre les lignes */
}

.ligne {
  display: flex;
  flex-direction: column;
  gap: 0.5rem; /* Garde l'espace entre le label et l'input */
}

.ligne label {
  font-weight: bold;
  color: white;
}

.ligne input,
.ligne select {
  padding: 0.75rem; /* Légèrement augmenté pour plus de confort */
  border: 1px solid var(--dark); /* Utilise la variable globale */
  border-radius: 0.375rem;
  font-size: 1rem;
  background-color: white; /* Fond blanc pour les inputs et selects */
  color: var(--dark); /* Couleur du texte dans les inputs (foncée pour contraster avec le blanc) */
}

.ligne input:focus,
.ligne select:focus {
  border-color: var(--primary); /* Utilise la variable globale */
  outline: none;
  box-shadow: 0 0 0 3px rgba(10, 58, 49, 0.2); /* Ombre légère au focus */
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem; /* Espace entre les colonnes de la grille */
}

.vehicule {
  background-color: white; /* Changé de #1a6f1a à white */
  padding: 1.5rem; /* Plus de padding */
  border-radius: 0.5rem;
  margin-top: 1.5rem; /* Plus de marge au-dessus */
  color: var(--dark); /* Pour que le texte à l'intérieur soit lisible sur fond blanc */
  border: 1px solid #eee; /* Ajout d'une bordure pour délimiter le cadre blanc */
  box-shadow: 0 2px 8px rgba(0,0,0,0.1); /* Ajout d'une ombre pour la profondeur */
}

.vehicule h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.25rem;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1); /* Bordure plus foncée pour le blanc */
  padding-bottom: 0.5rem;
}

/* Les styles spécifiques aux radio buttons ne sont plus nécessaires */
/*
.vehicle-type-selection .radio-group {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.vehicle-type-selection label {
  font-weight: normal; 
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}
*/

.bouton {
  background-color: var(--primary); /* Utilise la variable globale pour le bouton */
  color: white; /* Utilise white pour le texte */
  padding: 15px 25px; /* Ajusté padding */
  border: none; /* Pas de bordure par défaut */
  border-radius: 0.375rem;
  cursor: pointer;
  align-self: center; /* Centré horizontalement */
  transition: background-color 0.2s ease, transform 0.2s ease; /* Ajout d'une transition pour le transform */
  margin-top: 1.5rem; /* Plus d'espace au-dessus du bouton */
  font-size: 1.1rem;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2); /* Légère ombre */
}

.bouton:hover {
  background-color: #082d26; /* Un vert plus foncé au survol, cohérent avec --primary */
  transform: translateY(-2px); /* Petit effet de soulèvement au survol */
  box-shadow: 0 4px 8px rgba(0,0,0,0.3); /* Ombre plus prononcée au survol */
}

.utile{
  border-radius: 20px;
  width: clamp(300px, 90%, 600px); /* Plus flexible pour les différentes tailles d'écran */
  background-color: var(--primary); /* Utilise la variable globale */
  margin: 20px auto; /* Centré horizontalement et espace vertical */
  padding: 20px; /* Padding interne pour ne pas coller les bords */
}

/* Responsive pour les petits écrans */
@media (max-width: 768px) {
  .profil-container {
    padding: 1rem; /* Moins de padding sur les petits écrans */
  }
  .titre {
    font-size: 2.2rem;
  }
  .grid {
    grid-template-columns: 1fr; /* Une seule colonne sur mobile */
  }
  .bouton {
    width: 100%; /* Bouton prend toute la largeur sur mobile */
    align-self: stretch; /* S'étire */
    margin-left: 0; /* Pas de marge gauche fixe sur mobile */
  }
  .vehicule {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .titre {
    font-size: 1.8rem;
  }
  .formulaire, .grid {
    gap: 1rem; /* Réduire un peu le gap sur les très petits écrans */
  }
}
</style>
