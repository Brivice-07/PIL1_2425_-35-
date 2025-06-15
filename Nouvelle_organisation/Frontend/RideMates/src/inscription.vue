<template>
  <div class="auth-page">
    <h1>MotoShare</h1>
    <div class="register-container">
      <div class="register-box">
        <h2>Créer un compte</h2>
        <form @submit.prevent="handleSubmit">
          <p class="register-info">
            Veuillez remplir les informations ci-dessous pour vous inscrire.
          </p>

          <label>
            <input v-model="form.nom" type="text" placeholder="Nom" required />
          </label>

          <label>
            <input v-model="form.prenom" type="text" placeholder="Prénom" required />
          </label>

          <label>
            <input v-model="form.telephone" type="tel" placeholder="Numéro de téléphone" required />
          </label>

          <label>
            <input v-model="form.email" type="email" placeholder="Adresse e-mail" required />
          </label>

          <label>
            <input v-model="form.password" type="password" placeholder="Mot de passe" required />
          </label>

          <!-- Nouvelle section pour la sélection du rôle avec <select> -->
          <div class="role-selection">
            <label for="role" class="role-title">Je suis :</label>
            <select id="role" v-model="form.role" class="role-dropdown" required>
              <option value="passager">Passager</option>
              <option value="conducteur">Conducteur</option>
            </select>
          </div>
          <!-- Fin de la nouvelle section -->

          <button type="submit">
            S'inscrire
          </button>

          <p class="login-link">
            Vous avez déjà un compte ?
            <router-link to="/connexion">Connectez-vous ici</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Inscription",
  data() {
    return {
      form: {
        nom: "",
        prenom: "",
        telephone: "",
        email: "",
        password: "",
        role: "passager" // Rôle par défaut
      }
    };
  },
  methods: {
    handleSubmit() {
      // Les données du formulaire d'inscription, incluant maintenant le rôle.
      console.log("Données du formulaire d'inscription :", this.form);
      // En production, ici vous enverriez ces données à votre backend pour créer l'utilisateur.
      // Si l'inscription réussit, vous pourriez par exemple connecter l'utilisateur
      // et le rediriger vers /accueil.
      
      // Pour la simulation :
      localStorage.setItem('isAuthenticated', 'true'); // Simule une connexion après inscription
      this.$router.push('/accueil'); // Redirige vers la page d'accueil après inscription simulée
    }
  }
};
</script>

<style scoped>
/* Styles spécifiques au composant d'inscription */
.register-box {
  background: #fff;
  color: #0A3A31;
  padding: 40px;
  border-radius: 6px;
  max-width: 300px;
  width: 100%;
  text-align: center;
  margin: 20px auto; /* Centre la boîte horizontalement */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 15px;
  color: #0A3A31;
}

.register-info {
  margin-bottom: 20px;
  font-size: 0.9em;
  line-height: 1.4;
}

label {
  display: block;
  width: 100%;
}

input {
  width: calc(100% - 16px);
  padding: 10px 8px;
  margin-bottom: 15px; /* Espace entre les champs */
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
  box-sizing: border-box;
}

input:focus {
  border-color: #0A3A31;
  outline: none;
}

/* Styles pour la sélection du rôle (dropdown) */
.role-selection {
  margin-bottom: 20px;
  text-align: left; /* Aligne le texte à gauche dans cette section */
}

.role-title {
  font-size: 0.9em;
  color: #0A3A31;
  margin-bottom: 10px;
  font-weight: bold;
  display: block; /* S'assure que le label prend sa propre ligne si nécessaire */
}

.role-dropdown {
  width: 100%; /* Prend toute la largeur disponible */
  padding: 10px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
  box-sizing: border-box;
  background-color: #fff; /* Fond blanc pour le dropdown */
  appearance: none; /* Supprime le style par défaut du navigateur */
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23000000%22%20d%3D%22M287%2C197.3L159.1%2C69.4c-3.1-3.1-8.2-3.1-11.3%2C0L5.4%2C197.3c-3.1%2C3.1-3.1%2C8.2%2C0%2C11.3s8.2%2C3.1%2C11.3%2C0L145.7%2C85.5c3.1-3.1%2C8.2-3.1%2C11.3%2C0L275.7%2C208.6c3.1%2C3.1%2C8.2%2C3.1%2C11.3%2C0C290.1%2C205.5%2C290.1%2C200.4%2C287%2C197.3z%22%2F%3E%3C%2Fsvg%3E'); /* Icône de flèche déroulante */
  background-repeat: no-repeat;
  background-position: right 8px center;
  background-size: 12px;
  cursor: pointer;
}

.role-dropdown:focus {
  border-color: #0A3A31;
  outline: none;
}

button {
  width: 100%;
  padding: 12px;
  background: #0A3A31;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1.1em;
  cursor: pointer;
  margin-top: 15px;
  transition: background 0.3s ease;
}

button:hover {
  background: #095046;
}

.login-link {
  margin-top: 20px;
  font-size: 0.9em;
}

.login-link a {
  color: #0A3A31;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.login-link a:hover {
  text-decoration: underline;
  color: #095046;
}
</style>
