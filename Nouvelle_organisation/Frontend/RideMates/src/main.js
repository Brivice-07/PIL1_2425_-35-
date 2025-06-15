import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Importe l'instance du routeur

// Importe la feuille de style Font Awesome globalement.
// Cela garantit que les icônes sont disponibles partout dans l'application.
import '@fortawesome/fontawesome-free/css/all.min.css';

// Crée l'application Vue
const app = createApp(App);

// Utilise le routeur dans l'application pour gérer la navigation
app.use(router);

// Monte l'application sur l'élément HTML avec l'ID "app"
app.mount('#app');
