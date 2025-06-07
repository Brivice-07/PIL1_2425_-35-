-- Création de la base
CREATE DATABASE Ifri_comotorage;
USE Ifri_comotorage;

-- Table des utilisateurs
CREATE TABLE utilisateurs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nom VARCHAR(100),
  prenoms VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  telephone VARCHAR(20) UNIQUE,
  mot_de_passe VARCHAR(255) NOT NULL UNIQUE,
  statut ENUM('conducteur', 'passager'),
  profil VARCHAR(255) DEFAULT NULL,
  point_de_depart VARCHAR(255),
  horaires VARCHAR(255)
);

-- Table des véhicules
CREATE TABLE vehicules (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_utilisateur INT NOT NULL,
  marque VARCHAR(100),
  modele VARCHAR(100),
  places INT CHECK (places > 0),
  FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id)
);

-- Table des trajets
CREATE TABLE trajets (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_utilisateur INT, 
  id_vehicule INT,
  point_de_depart VARCHAR(255),
  point_arrivee VARCHAR(255),
  heure_depart TIME,
  places_disponibles INT CHECK (places_disponibles > 0),
  date_trajet DATE,
  niveau ENUM('actif', 'terminé', 'annulé') DEFAULT 'actif',
  latitude DECIMAL(9,6),
  longitude DECIMAL(9,6),
  FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id),
  FOREIGN KEY (id_vehicule) REFERENCES vehicules(id)
);

-- Table des demandes de covoiturage par passagers
CREATE TABLE demandes (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_utilisateur INT NOT NULL,
  point_de_depart VARCHAR(255),
  point_arrivee VARCHAR(255),
  heure_depart TIME,
  date_trajet DATE,
  FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id)
);

-- Table de la messagerie
CREATE TABLE messages (
  id INT PRIMARY KEY AUTO_INCREMENT,
  sender_id INT,
  receiver_id INT,
  contenu TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES utilisateurs(id),
  FOREIGN KEY (receiver_id) REFERENCES utilisateurs(id)
);

-- Table des notifications
CREATE TABLE notifications (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_utilisateur INT,
  message TEXT,
  etat ENUM ('envoyé', 'lu') DEFAULT 'envoyé',
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id)
);

-- Table des avis
CREATE TABLE avis (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_auteur INT NOT NULL,
  id_destinataire INT NOT NULL,
  note INT NOT NULL CHECK(note BETWEEN 1 AND 5),
  commentaire TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_auteur) REFERENCES utilisateurs(id),
  FOREIGN KEY (id_destinataire) REFERENCES utilisateurs(id)
);

-- Table des conducteurs
CREATE TABLE conducteurs(
id INT PRIMARY KEY AUTO_INCREMENT,
latitude DECIMAL(9,6) NOT NULL,
longitude DECIMAL (9,6) NOT NULL,
places_disponibles INT NOT NULL CHECK(places_disponibles > 0),
distance_max_detour FLOAT DEFAULT 5.0
);

-- Table des matching conducteur-passager
CREATE TABLE matching (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_trajet INT NOT NULL,
  id_conducteur INT NOT NULL,
  id_passager INT NOT NULL,
  situation ENUM('en attente', 'accepté', 'refusé', 'terminé') DEFAULT 'en attente',
  match_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  date_fin_match DATETIME,
  FOREIGN KEY (id_trajet) REFERENCES trajets(id),
  FOREIGN KEY (id_conducteur) REFERENCES utilisateurs(id),
  FOREIGN KEY (id_passager) REFERENCES utilisateurs(id)
);

-- Table de réinitialisation de mot de passe
CREATE TABLE reinitialisations_mot_de_passe (
  id INT PRIMARY KEY AUTO_INCREMENT,
  id_utilisateur INT NOT NULL,
  token VARCHAR(255) UNIQUE NOT NULL,
  expiration DATETIME NOT NULL,
  FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id)
);

-- Index
CREATE INDEX idx_utilisateur_contact ON utilisateurs(email, telephone);
CREATE INDEX idx_matching_situation ON matching(situation, match_date);
