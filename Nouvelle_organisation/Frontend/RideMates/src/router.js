import { createRouter, createWebHistory } from 'vue-router';

// Importe tous les composants de vos pages
// Les chemins d'importation ont été ajustés selon votre nouvelle structure de fichiers.
import Connexion from './connexion.vue';
import Inscription from './inscription.vue';
import MotDePasse from './motdepasse.vue';
import Accueil from './accueil.vue';
import Trajets from './trajets.vue';
import Profil from './profil.vue';
import Messagerie from './messagerie.vue'; // <-- Nouvelle importation du composant Messagerie.vue

// Définit les chemins (routes) de votre application
const routes = [
  {
    path: '/',
    // Quand quelqu'un arrive sur l'adresse principale (/), on le redirige.
    // Si l'utilisateur est déjà connecté, il va sur la page d'accueil.
    // Sinon, il va sur la page de connexion.
    redirect: to => {
      const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
      return isAuthenticated ? '/accueil' : '/connexion';
    }
  },
  {
    path: '/connexion',
    name: 'Connexion',
    component: Connexion
  },
  {
    path: '/inscription',
    name: 'Inscription',
    component: Inscription
  },
  {
    path: '/motdepasse',
    name: 'MotDePasse',
    component: MotDePasse
  },
  {
    path: '/accueil',
    name: 'Accueil',
    component: Accueil,
    meta: { requiresAuth: true } // Cette page nécessite une authentification
  },
  {
    path: '/trajets',
    name: 'Trajets',
    component: Trajets,
    meta: { requiresAuth: true } // Cette page nécessite une authentification
  },
  { // <-- Nouvelle route pour la page du profil
    path: '/profil',
    name: 'Profil',
    component: Profil,
    meta: { requiresAuth: true } // Cette page nécessite une authentification
  },
  { // <-- Nouvelle route pour la messagerie
    path: '/messagerie',
    name: 'Messagerie',
    component: Messagerie,
    meta: { requiresAuth: true } // Cette page nécessite une authentification
  },
];

// Crée le "routeur" qui va gérer la navigation
const router = createRouter({
  history: createWebHistory(), // Utilise une façon propre de gérer l'historique des adresses web (sans #)
  routes, // Lui dit quelles sont les pages et leurs chemins
});

// C'est une "garde" qui vérifie des choses avant chaque changement de page.
// Elle est exécutée avant chaque navigation pour vérifier l'authentification.
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !isAuthenticated) {
    // Si la page demande une connexion MAIS que l'utilisateur n'est PAS connecté
    console.log('Vous devez être connecté pour voir cette page. Redirection vers la page de connexion.');
    next('/connexion'); // On le renvoie vers la page de connexion
  } else if (isAuthenticated && (to.path === '/connexion' || to.path === '/inscription' || to.path === '/motdepasse')) {
    // Si l'utilisateur EST connecté MAIS qu'il essaie d'aller sur les pages de connexion, inscription ou mot de passe oublié
    console.log('Vous êtes déjà connecté. Redirection vers la page d\'accueil.');
    next('/accueil'); // On le renvoie vers la page d'accueil
  } else {
    // Dans tous les autres cas (tout va bien), on le laisse aller à la page demandée
    next();
  }
});

export default router; // On exporte le routeur pour que main.js puisse l'utiliser
