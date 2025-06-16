<template>
  <div class="auth-page">
    <h1>RideMates</h1>
    <div class="login-container">
      <div class="login-box">
        <h2>Bienvenue !</h2>
        <form @submit.prevent="handleLogin">
          <p>Connectez-vous avec votre <strong>email</strong> ou <strong>numéro de téléphone</strong>.</p>

          <label>
            <input v-model="form.emailOrTel" type="text" placeholder="Email ou Numéro de téléphone" required />
          </label>

          <label>
            <input v-model="form.password" type="password" placeholder="Mot de passe" required />
          </label>

          <div class="pwd">
            <router-link to="/motdepasse">Mot de passe oublié ?</router-link>
          </div>

          <button type="submit">
            Se connecter
          </button>

          <!-- Message d'erreur ou de succès -->
          <p v-if="message" :class="{'error-message': isError, 'success-message': !isError}">
            {{ message }}
          </p>

          <p class="signup-link">
            Créer un nouveau compte.
            <router-link to="/inscription">Cliquez ici</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Connexion",
  data() {
    return {
      form: {
        emailOrTel: "",
        password: "",
      },
      message: "",   // Pour afficher les messages à l'utilisateur
      isError: false // Pour contrôler le style du message (erreur ou succès)
    };
  },
  methods: {
    async handleLogin() {
      this.message = ""; // Réinitialise le message
      this.isError = false; // Réinitialise le statut d'erreur

      try {
        // --- DÉBUT DE LA SIMULATION DE CONNEXION ---
        // En production, cette partie ferait un appel à une API (ex: Axios.post('/api/login', this.form))
        // et vérifierait les identifiants sur le serveur.
        
        // Simule un petit délai pour montrer un comportement asynchrone
        await new Promise(resolve => setTimeout(resolve, 500)); 

        // Exemple de vérification (très basique pour la simulation)
        if (this.form.emailOrTel === 'test@example.com' && this.form.password === 'password123') {
          localStorage.setItem('isAuthenticated', 'true'); // Stocke l'état d'authentification
          this.message = "Connexion réussie ! Redirection...";
          // Redirection vers la page d'accueil
          await this.$router.push('/accueil');
        } else {
          // Si les identifiants ne correspondent pas à notre simulation
          this.isError = true;
          this.message = "Email/téléphone ou mot de passe incorrect.";
        }

        // --- FIN DE LA SIMULATION DE CONNEXION ---
        
      } catch (error) {
        console.error("Échec de la connexion :", error);
        this.isError = true;
        this.message = "Une erreur inattendue est survenue lors de la connexion.";
      }
    }
  }
};
</script>

<style scoped>
/* Styles spécifiques au composant de connexion */
.login-box {
  background: #fff;
  color: #0A3A31;
  padding: 40px;
  border-radius: 6px;
  max-width: 300px;
  width: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Petite ombre pour un effet 3D */
}

h2 {
  margin-bottom: 15px;
  color: #0A3A31;
}

form p {
  margin-bottom: 20px;
  font-size: 0.95em;
  line-height: 1.4;
}

label {
  display: block; /* Chaque label prend sa propre ligne */
  width: 100%;
}

input {
  width: calc(100% - 16px); /* Prend toute la largeur moins le padding */
  padding: 10px 8px;
  margin: 8px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
  box-sizing: border-box; /* Inclut padding et border dans la largeur totale */
}

input:focus {
  border-color: #0A3A31; /* Bordure plus foncée au focus */
  outline: none; /* Supprime le contour par défaut du navigateur */
}

.pwd {
  margin: 10px; /* Plus d'espace sous le lien mot de passe oublié */
  text-align: right;
}

.pwd a {
  color: #0A3A31;
  text-decoration: none;
  font-size: 0.9em;
  transition: color 0.3s ease; /* Transition douce pour le survol */
}

.pwd a:hover {
  text-decoration: underline;
  color: #095046; /* Changement de couleur au survol */
}

button {
  width: 100%;
  padding: 12px; /* Padding légèrement plus grand pour le bouton */
  background: #0A3A31;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1.1em; /* Taille de police légèrement plus grande */
  cursor: pointer;
  margin-top: 15px; /* Plus d'espace au-dessus du bouton */
  transition: background 0.3s ease; /* Transition douce pour le survol */
}

button:hover {
  background: #095046;
}

.signup-link {
  margin-top: 20px; /* Plus d'espace au-dessus du lien d'inscription */
  font-size: 0.9em;
}

.signup-link a {
  color: #0A3A31;
  text-decoration: none;
  font-weight: bold; /* Le lien est en gras */
  transition: color 0.3s ease;
}

.signup-link a:hover {
  text-decoration: underline;
  color: #095046;
}

.error-message {
  color: #e74c3c; /* Rouge pour les messages d'erreur */
  margin-top: 10px;
  font-weight: bold;
}

.success-message {
  color: #27ae60; /* Vert pour les messages de succès */
  margin-top: 10px;
  font-weight: bold;
}
</style>
