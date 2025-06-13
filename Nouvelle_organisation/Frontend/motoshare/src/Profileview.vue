<template>
      <h2 class="titre"> Mon Profil</h2>
  <div class="utile">

  <section class="profil-container">
    
    
    <!-- Formulaire -->
    <form @submit.prevent="handleSubmit" class="formulaire">
      <!-- Nom et prénom -->
      <div class="ligne">
        <label>Nom et prénom</label>
        <input v-model="profile.name" type="text" required />
      </div>

      <!-- Email -->
      <div class="ligne">
        <label>Email</label>
        <input v-model="profile.email" type="email" required />
      </div>

      <!-- Téléphone -->
      <div class="ligne">
        <label>Téléphone</label>
        <input v-model="profile.phone" type="tel" required />
      </div>

      <!-- Rôle -->
      <div class="ligne">
        <label>Rôle</label>
        <select v-model="profile.role">
          <option value="conducteur">Conducteur</option>
          <option value="passager">Passager</option>
        </select>
      </div>

      <!-- Informations véhicule (si conducteur) -->
      <div v-if="profile.role === 'conducteur'" class="vehicule">
        <h3>Informations du véhicule</h3>
        <div class="grid">
          <div class="ligne">
            <label>Marque et modèle</label>
            <input v-model="profile.vehicle.makeModel" type="text" />
          </div>
          <div class="ligne">
            <label >Nombre de places disponibles</label>
            <input v-model.number="profile.vehicle.seats" type="number" min="1" max="10" />
          </div>
        </div>
      </div>

      <!-- Bouton d'enregistrement-->
      <button type="submit" class="bouton">Enregistrer les modifications</button>
    </form>
    
  </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const profile = ref({
  name: 'AMOUSSOU Bénita',
  email: 'benitabeni@gmail.com',
  phone: '+229 47 97 13 04',
  role: 'conducteur',
  departure: 'Cotonou - Quartier 1',
  morningTime: '06:30',
  eveningTime: '18:00',
  vehicle: {
    makeModel: 'highlander',
    seats: 4
  }
})

function handleSubmit() {
  console.log('Profil mis à jour:', profile.value)
}
</script>

<style scoped>
.profil-container {
  max-width: 800px;
  margin: auto;
  padding: 2rem;
}

.titre {
  font-size: 3rem;
  font-weight: 90px;
  text-align: center;
  margin-bottom: 1.5rem;
  margin-right: 20px;

}

.formulaire {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.ligne {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  
}

.ligne label {
  font-weight: bold;
  color:white;
}


.ligne input,
.ligne select {
  padding: 0.5rem;
  border: 2px solid black;
  border-radius: 0.375rem;
  font-size: 1rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.vehicule {
  background-color:rgb(14, 95, 14);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}

.bouton {
  background-color: #13781f;
  color:beige;
  padding: 15px;
  border: 2px;
  border-radius: 0.375rem;
  cursor: pointer;
  align-self: flex-start;
  transition: background-color 0.2s ease;
  margin-left: 160px;

}

.bouton:hover {
  background-color: #2563eb;
 }
 .utile{
  border-radius: 20px;
  width: 600px;
  background-color:#0A3A31;
  justify-self:center ;
 }
 
  
 
 
 
 

 
 

 
</style>