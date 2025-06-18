<template>
  <div class="auth-page">
    <h1>RideMates</h1>
    <div class="forgot-container">
      <div class="forgot-box">
        <h2>Mot de passe oublié</h2>
        <p>Entrez votre email et nous vous enverrons un lien de réinitialisation.</p>
        <form @submit.prevent="handleSubmit">
          <input v-model="form.email" type="email" placeholder="Adresse e-mail" required />
          <button type="submit">Envoyer</button>
        </form>

        <!-- Affiche le message de confirmation directement dans l'interface -->
        <p v-if="message" class="info-message">{{ message }}</p>

        <p class="login-link">
          Retour à la connexion.
          <router-link to="/connexion">Cliquez ici</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MotDePasse",
  data() {
    return {
      form: {
        email: ""
      },
      message: "" // Nouvelle propriété pour afficher le message à l'utilisateur
    };
  },
  methods: {
    handleSubmit() {
      console.log("Demande de réinitialisation pour :", this.form.email);
      // En production, vous enverriez ici une requête à votre backend
      // pour envoyer l'e-mail de réinitialisation.

      // Simulation de l'envoi d'un lien
      this.message = `Un lien de réinitialisation a été envoyé à ${this.form.email}. Vérifiez votre boîte de réception.`;
      
      // Nettoie le formulaire et le message après un court délai
      setTimeout(() => {
        this.form.email = '';
        this.message = '';
      }, 3000); // Le message disparaît après 3 secondes
    }
  }
};
</script>

<style scoped>
/* Styles spécifiques au composant mot de passe oublié */
.forgot-box {
  background: #fff;
  color: #0A3A31;
  padding: 40px;
  border-radius: 6px;
  max-width: 300px;
  width: 100%;
  text-align: center;
  margin: 20px auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 15px;
  color: #0A3A31;
}

input {
  width: calc(100% - 16px);
  padding: 10px 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
  box-sizing: border-box;
}

input:focus {
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

.info-message {
  margin-top: 15px;
  color: #27ae60; /* Vert pour les messages d'information/succès */
  font-weight: bold;
}
</style>
