<template>
  <div class="messagerie-container">
    <!-- Colonne des conversations -->
    <div class="conversations-sidebar">
      <div class="sidebar-header">
        <!-- Bouton de retour ajouté ici -->
        <button @click="goBack" class="back-button">
          <i class="fas fa-arrow-left"></i>
        </button>
        <h2>RideMates-Messagerie</h2>
      </div>
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchTerm" 
          placeholder="Rechercher une conversation..."
        >
      </div>

      <div class="conversations-list">
        <div 
          v-for="(conv, userId) in filteredConversations" 
          :key="userId"
          :class="['conversation', { 'active': userId === currentUser }]"
          @click="loadConversation(userId)"
        >
          <div class="avatar">{{ conv.avatar }}</div>
          <div class="conversation-info">
            <h3>{{ conv.name }}</h3>
            <p :class="['message-preview', { 'draft': conv.draftMessage }]">
              {{ conv.draftMessage ? `Brouillon: ${conv.draftMessage}` : (conv.messages.length > 0 ? conv.messages[conv.messages.length - 1].text : 'Aucun message') }}
            </p>
          </div>
        </div>
        <p v-if="Object.keys(filteredConversations).length === 0" class="no-conversations">
          Aucune conversation trouvée.
        </p>
      </div>
    </div>

    <!-- Zone de chat -->
    <div class="chat-area">
      <div v-if="currentUser" class="chat-header">
        <div class="avatar">{{ currentConversation.avatar }}</div>
        <h2 id="chat-title">{{ currentConversation.name }} - {{ currentConversation.ride }}</h2>
      </div>
      <div v-else class="chat-header no-conversation-selected">
        <h2>Sélectionnez une conversation</h2>
      </div>

      <div class="messages-container" id="messages-container">
        <div v-if="currentUser">
          <div 
            v-for="(msg, index) in currentConversation.messages" 
            :key="index"
            :class="['message', msg.type]"
          >
            <p>{{ msg.text }}</p>
            <div class="message-time">{{ msg.time }}</div>
          </div>
        </div>
        <div v-else class="no-messages-placeholder">
          <i class="fas fa-comments"></i>
          <p>Commencez une nouvelle conversation ou sélectionnez-en une existante.</p>
        </div>
      </div>

      <div class="message-input-area" v-if="currentUser">
        <button class="btn-attachment"><i class="fas fa-paperclip"></i></button>
        <input 
          type="text" 
          v-model="messageInput" 
          placeholder="Écrivez un message..."
          @keypress.enter="sendMessage"
        >
        <button class="btn-send" @click="sendMessage"><i class="fas fa-paper-plane"></i></button>
      </div>
      <div class="message-input-area disabled" v-else>
        <input type="text" placeholder="Sélectionnez une conversation pour taper un message..." disabled>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Messagerie",
  data() {
    return {
      conversations: {
        // Toutes les conversations sont retirées pour commencer sans exemples
        // Elles seront ajoutées dynamiquement si nécessaire (ex: via une API)
      },
      currentUser: null, // Pas de conversation sélectionnée par défaut
      messageInput: '', // Le contenu du champ de saisie du message
      searchTerm: '' // Le terme de recherche pour filtrer les conversations
    };
  },
  computed: {
    // Renvoie l'objet de la conversation actuellement sélectionnée
    currentConversation() {
      // Retourne un objet vide si currentUser est null pour éviter les erreurs
      return this.currentUser ? this.conversations[this.currentUser] : {
        name: 'Chargement...', ride: '', avatar: '?' , messages: []
      };
    },
    // Renvoie les conversations filtrées en fonction du searchTerm
    filteredConversations() {
      const normalizedFilter = this.searchTerm.toLowerCase();
      const filtered = {};
      for (const userId in this.conversations) {
        const conv = this.conversations[userId];
        const matchesSearch = 
          conv.name.toLowerCase().includes(normalizedFilter) ||
          conv.ride.toLowerCase().includes(normalizedFilter) ||
          (conv.draftMessage && conv.draftMessage.toLowerCase().includes(normalizedFilter)) ||
          (conv.messages.length > 0 && conv.messages[conv.messages.length - 1].text.toLowerCase().includes(normalizedFilter));

        if (matchesSearch || this.searchTerm === '') {
          filtered[userId] = conv;
        }
      }
      return filtered;
    }
  },
  watch: {
    // Surveille les changements dans l'input du message pour sauvegarder le brouillon
    messageInput(newValue) {
      if (this.currentConversation && this.currentUser) { // Vérifie aussi si une conversation est sélectionnée
        this.currentConversation.draftMessage = newValue;
      }
    },
    // Surveille le changement de conversation pour défiler vers le bas
    currentUser(newVal, oldVal) {
      if (newVal) { // S'il y a une nouvelle conversation sélectionnée
        this.$nextTick(() => {
          const messagesContainer = document.getElementById('messages-container');
          if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
          }
        });
      }
    }
  },
  methods: {
          // Méthode pour naviguer vers la page précédente (ou la page d'accueil si aucune historique)
      goBack() {
        // Si l'historique du navigateur le permet, revenir en arrière
        if (window.history.length > 1) {
          this.$router.go(-1);
        } else {
          // Sinon, naviguer explicitement vers la page d'accueil
          this.$router.push('/'); // Assurez-vous que '/' est la route de votre page Accueil.vue
        }
      },
    // Charge une conversation spécifique
    loadConversation(userId) {
      // Sauvegarder le brouillon de la conversation précédente AVANT de changer d'utilisateur
      if (this.currentUser && this.conversations[this.currentUser]) {
        this.conversations[this.currentUser].draftMessage = this.messageInput;
      }

      this.currentUser = userId; // Met à jour l'utilisateur actif
      this.messageInput = this.currentConversation.draftMessage; // Charge le brouillon de la nouvelle conversation
    },
    
    // Envoie un message
    sendMessage() {
      if (!this.currentUser) return; // Ne rien faire si aucune conversation n'est sélectionnée

      const text = this.messageInput.trim();
      
      if (text) {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        // Ajoute le message à l'objet conversation
        this.currentConversation.messages.push({
          type: "sent",
          text: text,
          time: timeString
        });
        
        // Vide le brouillon pour cette conversation après l'envoi
        this.currentConversation.draftMessage = ""; 
        this.messageInput = ''; // Vide le champ de saisie
        
        // Défile vers le bas après l'envoi du message
        this.$nextTick(() => {
          const messagesContainer = document.getElementById('messages-container');
          if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
          }
        });
      }
    }
  },
  mounted() {
    // Au lieu de charger une conversation par défaut, on commence sans rien
    // Si vous souhaitez charger une conversation par défaut si elle existe (ex: la première dans `conversations`),
    // vous pouvez ajouter une logique ici :
    // const firstUserId = Object.keys(this.conversations)[0];
    // if (firstUserId) {
    //   this.loadConversation(firstUserId);
    // }
  }
};
</script>

<style scoped>
/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', sans-serif;
}

.messagerie-container {
    height: 100vh;
    display: flex;
    background-color: #f5f5f5;
}

/* Sidebar des conversations */
.conversations-sidebar {
    width: 350px;
    background-color: white;
    border-right: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
}

.sidebar-header {
    padding: 15px;
    background-color: var(--primary); /* Utilisation de la variable globale */
    color: white;
    text-align: center;
    font-weight: bold;
}

/* Styles pour le bouton de retour */
.back-button {
    position: absolute; /* Positionne le bouton par rapport au header */
    left: 15px; /* Aligné à gauche */
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: white;
    font-size: 24px;
    cursor: pointer;
    padding: 5px;
    border-radius: 50%;
    transition: background-color 0.2s ease-in-out;
    display: flex; /* Pour centrer l'icône */
    align-items: center;
    justify-content: center;
}

.back-button:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.search-bar {
    padding: 15px;
    border-bottom: 1px solid #eee;
}

.search-bar input {
    width: 100%;
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 20px;
    background-color: #f5f5f5;
}

.conversations-list {
    flex: 1;
    overflow-y: auto;
    padding-top: 10px; /* Ajoute un peu d'espace en haut */
}

.conversation {
    display: flex;
    padding: 15px;
    border-bottom: 1px solid #f5f5f5;
    cursor: pointer;
    transition: background-color 0.2s;
}

.conversation:hover {
    background-color: #f0f0f0;
}

.conversation.active {
    background-color: #e1f5ee;
    border-left: 3px solid var(--primary); /* Utilisation de la variable globale */
}

.avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: var(--primary); /* Utilisation de la variable globale */
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-right: 15px;
    flex-shrink: 0; /* Empêche l'avatar de se rétrécir */
}

.conversation-info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.conversation-info h3 {
    font-size: 16px;
    margin-bottom: 5px;
    color: var(--dark); /* Utilisation de la variable globale */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.message-preview {
    color: #666;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 14px;
}

.message-preview.draft {
    color: #d8a04b; /* Couleur directe ou autre variable si définie */
    font-style: italic;
}

.no-conversations {
  text-align: center;
  color: #888;
  padding: 20px;
  font-style: italic;
}


/* Zone de chat principale */
.chat-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: white;
}

.chat-header {
    padding: 15px;
    background-color: var(--primary); /* Utilisation de la variable globale */
    color: white;
    border-bottom: 1px solid #eee;
    display: flex;
    align-items: center;
}

.chat-header.no-conversation-selected {
  justify-content: center;
  font-style: italic;
  font-size: 1.2em;
}

.chat-header .avatar {
    margin-right: 15px;
    background-color: white;
    color: var(--primary); /* Utilisation de la variable globale */
}

.chat-header h2 {
    font-size: 18px;
}

.messages-container {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background-color: #f5f5f5;
    background-image: url('https://www.transparenttextures.com/patterns/motorcycle.png');
    background-blend-mode: overlay;
    display: flex; /* Utilisation de flexbox pour aligner les messages */
    flex-direction: column;
    justify-content: flex-end; /* Aligne les messages en bas par défaut */
}

.no-messages-placeholder {
  text-align: center;
  color: #aaa;
  font-size: 1.1em;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%; /* S'assure que le placeholder est centré verticalement */
}

.no-messages-placeholder i {
  font-size: 3em;
  margin-bottom: 15px;
  color: #ccc;
}

.message {
    max-width: 70%;
    margin-bottom: 15px;
    padding: 12px 16px;
    border-radius: 18px;
    position: relative;
    box-shadow: 0 1px 1px rgba(0,0,0,0.1);
}

.received {
    background: white;
    align-self: flex-start; /* Aligne à gauche */
    border-top-left-radius: 0;
}

.sent {
    background: var(--primary); /* Utilisation de la variable globale */
    color: white;
    align-self: flex-end; /* Aligne à droite */
    border-top-right-radius: 0;
}

.message-time {
    font-size: 11px;
    color: rgba(255,255,255,0.7);
    margin-top: 5px;
    text-align: right;
}

.received .message-time {
    color: rgba(0,0,0,0.5);
}

.message-input-area {
    padding: 15px;
    display: flex;
    border-top: 1px solid #eee;
    background-color: white;
    align-items: center;
}

.message-input-area.disabled {
    background-color: #f0f0f0;
    border-top: 1px solid #ddd;
    cursor: not-allowed;
}

.message-input-area input {
    flex: 1;
    padding: 12px 15px;
    border: 1px solid #ddd;
    border-radius: 25px;
    margin: 0 10px;
    outline: none;
    transition: border 0.3s;
}

.message-input-area input:focus:not(:disabled) {
    border-color: var(--primary); /* Utilisation de la variable globale */
}

.message-input-area input:disabled {
    background-color: #e9e9e9;
    cursor: not-allowed;
    color: #888;
}

.btn-attachment, .btn-send {
    /* Styles pour les boutons actifs */
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 18px;
}

/* Styles pour les boutons désactivés */
.message-input-area.disabled .btn-attachment,
.message-input-area.disabled .btn-send {
    background-color: #ccc;
    color: #666;
    cursor: not-allowed;
}

.btn-attachment:hover:not(:disabled) {
    color: var(--primary); /* Utilisation de la variable globale */
}

.btn-send:hover:not(:disabled) {
    background-color: #0c4b3f; /* Teinte plus foncée directe, ou utiliser une variable si elle existe */
    transform: scale(1.05);
}

/* Responsive */
@media (max-width: 768px) {
    .messagerie-container {
        flex-direction: column;
    }
    .conversations-sidebar {
        width: 100%;
        height: 40vh; /* Moins de hauteur sur mobile */
        border-right: none;
        border-bottom: 1px solid #e0e0e0;
    }
    .chat-area {
        flex: 1; /* Prend le reste de l'espace vertical */
    }
    .messages-container {
        padding: 15px;
    }
    .message {
        max-width: 85%; /* Plus large sur mobile */
    }
}

@media (max-width: 480px) {
  .sidebar-header h2 {
    font-size: 1.2em;
  }
  .search-bar input {
    padding: 8px 12px;
  }
  .conversation {
    padding: 10px;
  }
  .avatar {
    width: 40px;
    height: 40px;
    font-size: 18px;
    margin-right: 10px;
  }
  .conversation-info h3 {
    font-size: 15px;
  }
  .message-preview {
    font-size: 13px;
  }
  .chat-header h2 {
    font-size: 16px;
  }
  .message-input-area input {
    padding: 10px 12px;
    margin: 0 5px;
  }
  .btn-send {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
  .btn-attachment {
    font-size: 18px;
    padding: 5px;
  }
}
</style>
