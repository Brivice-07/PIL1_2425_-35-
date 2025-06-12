import { createRouter, createWebHistory } from 'vue-router';
import Connexion from './connexion.vue';
import Inscription from './inscription.vue';
import Motdepasse from './motdepasse.vue';


const routes = [
  { path: '/', redirect: '/connexion' },
  { path: '/connexion', component: Connexion },
  { path: '/inscription', component: Inscription },
  { path: '/motdepasse', component: Motdepasse },
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
