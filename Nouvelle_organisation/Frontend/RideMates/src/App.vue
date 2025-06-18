<template>
  <div>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  watch: {
    $route(to) {
      // Double vérification de l'authentification
      if (localStorage.getItem('isAuthenticated') === 'true' 
          && to.path === '/connexion') {
        this.$router.replace('/accueil');
      }
    }
  }
};
</script>

<style>
/* Styles globaux (non-scoped) */
body {
  margin: 0;
  padding: 0;
  font-family: 'Arial', sans-serif;
  min-height: 100vh;
}

/* Style de base pour les pages d'authentification */
.auth-page {
  background-color: #0A3A31;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  text-align: center;
}

/* Variables CSS globales, déplacées ici pour être accessibles partout */
:root {
  --primary: #0A3A31;
  --secondary: #E67E22; /* Couleur orange pour la moto / alertes */
  --car-color: #3498db; /* Couleur bleue pour la voiture */
  --light: #f8f9fa;
  --dark: #343a40;
  --hover-color: rgba(255, 255, 255, 0.2);
  --btn-color: #2c3e50; /* Couleur pour les boutons primaires d'Accueil */
}
</style>
