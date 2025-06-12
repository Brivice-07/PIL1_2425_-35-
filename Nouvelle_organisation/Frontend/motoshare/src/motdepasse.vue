<template>
  <div>
    <h1>MotoShare</h1>
    <div class="forgot-box">
      <h2>Mot de passe oublié</h2>
      <p>Entrez votre email et nous vous enverrons un lien de réinitialisation.</p>
        <form @submit.prevent="handleSubmit">
            <input v-model="form.email" type="email" placeholder="Adresse e-mail" required />
            <button type="submit">Envoyer</button>
        </form>

        <p class="signup-link">
            Retour a la connexion.
            <router-link to="/connexion">Cliquez ici</router-link>
        </p>

    </div>
  </div>
</template>

<script>
    export default {
        data() {
            return {
            form: { email: "" }
            };
        },
        methods: {
            handleSubmit() {
            alert(`Lien envoyé à ${this.form.email}`);
            // ici ta logique d'envoi
            }
        }
    };
</script>

<style scoped>
@import "/src/assets/motdepasse.css";
</style>
