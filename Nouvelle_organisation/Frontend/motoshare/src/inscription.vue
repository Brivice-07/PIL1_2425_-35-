<template>
  <!-- Contenu principal de la page -->
    <div>
        <!-- Titre principal -->
        <h1>MotoShare</h1>

        <!-- Conteneur global du formulaire -->
        <div class="register-container">
        <div class="register-box">
            <!-- Sous-titre -->
            <h2>Créer un compte</h2>

            <!-- Formulaire d'inscription -->
            <form @submit.prevent="handleSubmit">
            <!-- Texte d'information -->
            <p class="register-info">
                Veuillez remplir les informations ci-dessous pour vous inscrire.
            </p>

            <!-- Champ Nom -->
            <label>
                <input v-model="form.nom" type="text" placeholder="Nom" required />
            </label>

            <!-- Champ Prénom -->
            <label>
                <input v-model="form.prenom" type="text" placeholder="Prénom" required />
            </label>

            <!-- Champ Numéro de téléphone -->
            <label>
                <input v-model="form.telephone" type="tel" placeholder="Numéro de téléphone" required />
            </label>

            <!-- Champ Email -->
            <label>
                <input v-model="form.email" type="email" placeholder="Adresse e-mail" required />
            </label>

            <!-- Champ Mot de passe -->
            <label>
                <input v-model="form.password" type="password" placeholder="Mot de passe" required />
            </label>

            <!-- Bouton d'envoi du formulaire -->
            <button type="submit">S'inscrire</button>

            <!-- Lien vers la page de connexion -->
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
  name: "Inscription", // Nom du composant
  data() {
    return {
      // Objet contenant les données du formulaire
      form: {
        nom: "",
        prenom: "",
        telephone: "",
        email: "",
        password: ""
      }
    };
  },
  methods: {
    // Méthode appelée lors de la soumission du formulaire
    handleSubmit() {
      // Ici tu pourrais envoyer les données à un serveur avec axios ou fetch
      console.log("Données du formulaire :", this.form);
      alert("Inscription soumise !");
    }
  }
};
</script>

<style scoped>
/* Importe le fichier CSS externe uniquement pour ce composant */
@import "/src/assets/inscription.css";
</style>
