<template>
  <div class="home-container">
    <header class="header">
      <nav class="navbar">
        <div class="nav-left">
          <div class="logo">
            <i class="fas fa-motorcycle"></i>
            <span>RideMates-Accueil</span>
          </div>
        </div>
        
        <div class="nav-center">
          <router-link to="/accueil" class="active"><i class="fas fa-home"></i> Accueil</router-link>
          <router-link to="/trajets"><i class="fas fa-route"></i> Trajets</router-link>
          <router-link to="/messagerie"><i class="fas fa-comment-alt"></i> Messages</router-link>
        </div>
        
        <div class="nav-right">
          <div class="profile-menu" @click="toggleDropdown">
            <i class="fas fa-user-circle"></i>
            <span class="profile-text">Mon compte</span>
            <i class="fas fa-chevron-down"></i>
            
            <div class="dropdown" v-if="showDropdown">
              <router-link to="/profil">
                <i class="fas fa-user"></i> Mon Profil
              </router-link>
              <a href="#" @click.prevent="logout">
                <i class="fas fa-sign-out-alt"></i> Déconnexion
              </a>
            </div>
          </div>
          
          <div class="menu-toggle" @click="toggleMobileMenu">
            <i class="fas fa-bars"></i>
          </div>
        </div>
      </nav>
      
      <!-- Menu Mobile -->
      <div class="mobile-menu" :class="{ 'active': showMobileMenu }">
        <router-link to="/accueil" @click="closeMobileMenu"><i class="fas fa-home"></i> Accueil</router-link>
        <router-link to="/trajets" @click="closeMobileMenu"><i class="fas fa-route"></i> Trajets</router-link>
        <router-link to="/messages" @click="closeMobileMenu"><i class="fas fa-comment-alt"></i> Messages</router-link>
        <router-link to="/profil" @click="closeMobileMenu"><i class="fas fa-user"></i> Mon Profil</router-link>
        <a href="./connexion.vue" @click.prevent="logoutAndCloseMobileMenu"><i class="fas fa-sign-out-alt"></i> Déconnexion</a>
      </div>
    </header>

    <main>
      <!-- Hero Section -->
      <section class="hero">
        <div class="hero-content">
          <h1>Partagez la route entre motards</h1>
          <p>MotoShare connecte les passionnés de moto pour des trajets plus économiques et conviviaux.</p>
          <div class="cta-buttons">
            <router-link to="/trajets" class="btn">
              <i class="fas fa-search"></i> Rechercher un covoiturage
            </router-link>
            <router-link to="/trajets" class="btn">
              <i class="fas fa-plus"></i> Proposer un covoiturage
            </router-link>
          </div>
        </div>
      </section>

      <!-- Section Comment ça marche -->
      <section class="how-it-works">
        <h2 class="section-title">Comment ça marche ?</h2>
        
        <div class="steps">
          <div class="step">
            <div class="step-icon">
              <i class="fas fa-user-plus"></i>
            </div>
            <h3>Créez votre profil</h3>
            <p>Inscrivez-vous en 2 minutes et complétez votre profil motard</p>
          </div>
          
          <div class="step">
            <div class="step-icon">
              <i class="fas fa-search"></i>
            </div>
            <h3>Trouvez un trajet</h3>
            <p>Recherchez des covoiturages correspondant à vos critères</p>
          </div>
          
          <div class="step">
            <div class="step-icon">
              <i class="fas fa-motorcycle"></i>
            </div>
            <h3>Partez à l'aventure</h3>
            <p>Contactez le conducteur et voyagez ensemble</p>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer>
      <div class="footer-container">
        <div class="footer-links">
          <h3>Liens rapides</h3>
          <ul>
            <li><router-link to="/accueil"><i class="fas fa-chevron-right"></i> Accueil</router-link></li>
            <li><router-link to="/trajets"><i class="fas fa-chevron-right"></i> Trajets</router-link></li>
            <li><router-link to="/messagerie"><i class="fas fa-chevron-right"></i> Messages</router-link></li>
            <li><router-link to="/profil"><i class="fas fa-chevron-right"></i> Profil</router-link></li>
          </ul>
        </div>
        
        <div class="footer-contact">
          <h3>Contactez-nous</h3>
          <p><i class="fas fa-map-marker-alt"></i> XXXXXXXXX</p>
          <p><i class="fas fa-phone"></i> +229 01XXXXXXXX</p>
          <p><i class="fas fa-envelope"></i> contact@ridemates.bj</p>
          
          <div class="social-links">
            <a href="#" target="_blank" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="#" target="_blank" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
            <a href="#" target="_blank" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
            <a href="#" target="_blank" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
          </div>
        </div>
      </div>
      
      <div class="copyright">
        &copy; 2025 Covoiturage. Tous droits réservés.
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Accueil',
  data() {
    return {
      showDropdown: false, // Contrôle la visibilité du menu déroulant du profil
      showMobileMenu: false, // Contrôle la visibilité du menu mobile
      notificationCount: 3, // Exemple de nombre de notifications
      fontAwesomeLink: null // Pour garder une référence à l'élément de lien créé
    }
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
      // Ferme le menu mobile si le menu déroulant du profil est ouvert
      if (this.showDropdown && this.showMobileMenu) {
        this.showMobileMenu = false;
      }
    },
    toggleMobileMenu() {
      this.showMobileMenu = !this.showMobileMenu;
      // Ferme le menu déroulant du profil si le menu mobile est ouvert
      if (this.showMobileMenu && this.showDropdown) {
        this.showDropdown = false;
      }
    },
    closeMobileMenu() {
      this.showMobileMenu = false; // Ferme le menu mobile après la navigation
    },
    logout() {
      console.log('Déconnexion de l\'utilisateur.');
      localStorage.removeItem('isAuthenticated'); // Efface l'état d'authentification
      this.$router.push('/connexion'); // Redirige vers la page de connexion
      this.showDropdown = false; // Ferme le menu déroulant après la déconnexion
    },
    logoutAndCloseMobileMenu() {
      this.logout();
      this.closeMobileMenu();
    },
    // Gérer les clics en dehors des menus pour les fermer
    handleClickOutside(event) {
      const profileMenu = this.$el.querySelector('.profile-menu');
      const mobileMenuToggle = this.$el.querySelector('.menu-toggle');
      const mobileMenu = this.$el.querySelector('.mobile-menu');

      // Fermer le dropdown si le clic n'est pas à l'intérieur du profile-menu
      if (profileMenu && !profileMenu.contains(event.target)) {
        this.showDropdown = false;
      }
      
      // Fermer le menu mobile si le clic n'est pas à l'intérieur du mobile-menu ou du menu-toggle
      if (mobileMenu && !mobileMenu.contains(event.target) && mobileMenuToggle && !mobileMenuToggle.contains(event.target)) {
        this.showMobileMenu = false;
      }
    }
  },
  mounted() {
    // Dynamiquement injecter le CSS de Font Awesome si ce n'est pas déjà présent
    // Attention : Pour les bibliothèques globales comme Font Awesome, la meilleure pratique
    // est généralement de les inclure dans le fichier public/index.html
    // ou de les importer dans votre main.js (si votre outil de compilation le permet).
    // Cette méthode est utilisée ici pour répondre à votre demande de ne pas toucher index.html.
    if (!document.querySelector('link[href*="font-awesome"]')) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css';
      document.head.appendChild(link);
      this.fontAwesomeLink = link; // Garde une référence pour pouvoir le retirer plus tard
    }

    // Ajoute un écouteur de clic global pour fermer les menus
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    // Retire le lien Font Awesome lorsque le composant est détruit (lorsque vous quittez la page d'accueil)
    if (this.fontAwesomeLink && document.head.contains(this.fontAwesomeLink)) {
      document.head.removeChild(this.fontAwesomeLink);
    }
    // Retire l'écouteur de clic global
    document.removeEventListener('click', this.handleClickOutside);
  }
}
</script>

<style scoped>
/* Variables CSS pour faciliter la gestion des couleurs */
:root {
  --primary: #0A3A31;
  --light: #f8f9fa;
  --dark: #343a40;
  --hover-color: rgba(255, 255, 255, 0.2);
  --btn-color: #2c3e50;
}

/* Styles globaux pour le composant */
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header */
.header {
  background-color: var(--primary);
  color: white;
  padding: 15px 20px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  position: relative; /* Pour le positionnement du menu mobile */
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-left, .nav-right {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.logo i {
  margin-right: 10px;
  color: white;
}

.nav-center {
  display: flex;
  align-items: center;
}

.nav-center a {
  color: white;
  text-decoration: none;
  margin: 0 15px;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-center a:hover {
  background-color: var(--hover-color);
}

.profile-menu {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.profile-menu:hover {
  background-color: var(--hover-color);
}

.profile-menu i:first-child {
  font-size: 1.8rem;
  margin-right: 8px;
}

.profile-menu i.fa-chevron-down {
  font-size: 0.8rem;
  margin-left: 5px;
}

.dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 5px;
  box-shadow: 0 3px 10px rgba(0,0,0,0.1);
  padding: 10px 0;
  min-width: 150px;
  /* display: none; */ /* Contrôlé par v-if */
  z-index: 100;
  margin-top: 5px; /* Petit espace entre le menu et le déclencheur */
}

.dropdown a {
  color: var(--dark);
  padding: 8px 15px;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap; /* Empêche le texte de se casser */
}

.dropdown a:hover {
  background: #f0f0f0;
}

/* Menu Hamburger */
.menu-toggle {
  display: none; /* Masqué par défaut sur desktop */
  cursor: pointer;
  font-size: 1.5rem;
  margin-left: 20px;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.menu-toggle:hover {
  background-color: var(--hover-color);
}

.mobile-menu {
  display: none; /* Masqué par défaut */
  position: absolute;
  top: 70px; /* Aligné sous le header */
  left: 0;
  width: 100%;
  background-color: var(--primary);
  padding: 1rem 0; /* Ajusté pour les liens */
  box-shadow: 0 5px 10px rgba(0,0,0,0.1);
  z-index: 99;
}

.mobile-menu.active {
  display: block; /* Affiché quand actif */
}

.mobile-menu a {
  display: flex;
  align-items: center;
  color: white;
  padding: 12px 20px; /* Plus de padding pour les éléments du menu mobile */
  text-decoration: none;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  transition: background-color 0.3s;
}

.mobile-menu a:last-child {
  border-bottom: none; /* Pas de bordure pour le dernier élément */
}

.mobile-menu a:hover {
  background-color: var(--hover-color);
}

.mobile-menu a i {
  margin-right: 10px;
}

/* Main Content */
main {
  flex: 1;
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

/* Hero Section */
.hero {
  background-color: var(--primary);
  color: white;
  padding: 3rem 2rem;
  border-radius: 10px;
  text-align: center;
  margin-bottom: 3rem;
  background-image: linear-gradient(to right, rgba(10, 58, 49, 0.9), rgba(10, 58, 49, 0.9));
  box-shadow: 0 5px 15px rgba(0,0,0,0.1); /* Ajout d'une ombre */
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero-content p {
  margin-bottom: 2rem;
  line-height: 1.6;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  opacity: 0.9;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap; /* Permet aux boutons de passer à la ligne sur petits écrans */
}

.btn {
  padding: 0.8rem 1.5rem;
  border-radius: 30px; /* Forme de pilule */
  font-weight: bold;
  text-decoration: none;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--btn-color);
  color: white;
  border: 2px solid var(--btn-color);
}

.btn:hover {
  background-color: #1a252f;
  transform: translateY(-2px);
  border-color: #1a252f;
}

/* Section Comment ça marche */
.how-it-works {
  background-color: white;
  border-radius: 10px;
  padding: 2.5rem; /* Augmentation du padding */
  box-shadow: 5px 15px 15px 20px rgba(0,0,0,0.05);
  margin-bottom: 3rem;
}

.section-title {
  text-align: center;
  margin-bottom: 2.5rem; /* Plus d'espace sous le titre */
  color: var(--primary);
  font-size: 2rem; /* Titre plus grand */
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.step {
  text-align: center;
  padding: 1.5rem;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.step:hover {
  transform: translateY(-5px); /* Effet au survol */
  background-color: antiquewhite;
}

.step-icon {
  width: 80px;
  height: 80px;
  background-color: rgba(10, 58, 49, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  box-shadow: 2px 10px 5px rgba(0,0,0,0.05);
}

.step h3 {
  margin-bottom: 0.5rem;
  color: var(--primary);
  font-size: 1.3rem;
}

.step p {
  color: #666;
  font-size: 0.95em;
}

/* Footer */
footer {
  background-color: var(--primary);
  color: white;
  padding: 2rem 1rem;
  margin-top: auto;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  padding-bottom: 2rem; /* Espace avant le copyright si pas de bordure */
}

.footer-links h3, .footer-contact h3 {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  position: relative;
  padding-bottom: 10px;
}

.footer-links h3::after, .footer-contact h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 50px;
  height: 2px;
  background-color: var(--btn-color);
}

.footer-links ul {
  list-style: none;
}

.footer-links li {
  margin-bottom: 0.8rem;
}

.footer-links a {
  color: white;
  text-decoration: none;
  opacity: 0.8;
  transition: opacity 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.footer-links a:hover {
  opacity: 1;
}

.footer-contact p {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 10px;
  opacity: 0.8;
}

.social-links {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.social-links a {
  color: white;
  background-color: rgba(255, 255, 255, 0.1);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  font-size: 1.1rem;
}

.social-links a:hover {
  background-color: var(--btn-color);
  transform: translateY(-3px);
}

.copyright {
  text-align: center;
  margin-top: 2rem; /* Réajustement de l'espace */
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  opacity: 0.7;
  font-size: 0.9rem;
}

/* Responsive */
@media (max-width: 992px) {
  .nav-center {
    display: none; /* Masque les liens de navigation principaux */
  }
  
  .menu-toggle {
    display: block; /* Affiche le bouton hamburger */
  }
  
  .footer-container {
    grid-template-columns: 1fr 1fr; /* 2 colonnes sur tablette */
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 2rem 1rem;
  }
  
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .cta-buttons {
    flex-direction: column; /* Boutons en colonne sur mobile */
    align-items: center;
  }
  
  .steps {
    grid-template-columns: 1fr; /* Une seule colonne pour les étapes */
  }
  
  .footer-container {
    grid-template-columns: 1fr; /* Une seule colonne pour le footer */
    text-align: center;
  }

  .footer-links h3::after, .footer-contact h3::after {
    left: 50%; /* Centre la ligne sous les titres du footer */
    transform: translateX(-50%);
  }

  .footer-contact p, .footer-links a {
    justify-content: center; /* Centre les éléments dans le footer */
  }
  .social-links {
    justify-content: center; /* Centre les icônes sociales */
  }
}
</style>
