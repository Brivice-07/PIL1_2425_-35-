<template>
  <div>
    <h1>MotoShare</h1>
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

          <button type="submit">Se connecter</button>
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
import { ref } from "vue";

export default {
  setup() {
    const form = ref({
      emailOrTel: "",
      password: "",
    });

        const handleLogin = () => {
            console.log("Tentative de connexion avec :", form.value);
  // Ajoute ici la logique de connexion (API, validation, etc.)
        };

     return { form, handleLogin };
    },
};
</script>

<style scoped>
@import "/src/assets/connexion.css";
</style>