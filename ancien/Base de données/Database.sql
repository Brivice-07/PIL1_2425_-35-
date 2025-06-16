-- Création de la base
CREATE DATABASE Ifri_comotorage;
USE Ifri_comotorage;

--Table users (Utilisateurs)
CREATE TABLE utilisateurs (
    id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    telephone VARCHAR(20) UNIQUE NOT NULL,
    mot_de_passe_hash VARCHAR(255) NOT NULL,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    photo_profil VARCHAR(255),
    role ENUM('conducteur', 'passager') NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Table user_profiles (Profils d’utilisateurs)
CREATE TABLE profils_utilisateurs (
    id_profil INT PRIMARY KEY AUTO_INCREMENT,
    id_utilisateur INT UNIQUE NOT NULL,
    adresse_depart TEXT NOT NULL,
    latitude_depart DECIMAL(10, 8) NOT NULL,
    longitude_depart DECIMAL(11, 8) NOT NULL,
    adresse_arrivee TEXT NOT NULL,
    latitude_arrivee DECIMAL(10, 8) NOT NULL,
    longitude_arrivee DECIMAL(11, 8) NOT NULL,
    heure_depart_habituelle TIME NOT NULL,
    heure_arrivee_habituelle TIME NOT NULL,
    modele_vehicule VARCHAR(100),
    nombre_places INT,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE
);

--Table rides (Trajets et demandes)
CREATE TABLE trajets (
    id_trajet INT PRIMARY KEY AUTO_INCREMENT,
    id_utilisateur INT NOT NULL,
    est_offre BOOLEAN NOT NULL, -- TRUE pour offre de covoiturage, FALSE pour demande
    adresse_depart TEXT NOT NULL,
    latitude_depart DECIMAL(10, 8) NOT NULL,
    longitude_depart DECIMAL(11, 8) NOT NULL,
    adresse_arrivee TEXT NOT NULL,
    latitude_arrivee DECIMAL(10, 8) NOT NULL,
    longitude_arrivee DECIMAL(11, 8) NOT NULL,
    heure_depart DATETIME NOT NULL,
    nombre_places_disponibles INT,
    statut ENUM('actif', 'terminé', 'annulé') DEFAULT 'actif',
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur)
);

--Table matches (Correspondances de covoiturage)
CREATE TABLE correspondances (
    id_correspondance INT PRIMARY KEY AUTO_INCREMENT,
    id_offre_trajet INT NOT NULL,
    id_demande_trajet INT NOT NULL,
    id_conducteur INT NOT NULL,
    id_passager INT NOT NULL,
    score_compatibilite DECIMAL(5, 2) NOT NULL, -- Score entre 0 et 100
    statut ENUM('en attente', 'accepté', 'refusé', 'terminé') DEFAULT 'en attente',
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_offre_trajet) REFERENCES trajets(id_trajet),
    FOREIGN KEY (id_demande_trajet) REFERENCES trajets(id_trajet),
    FOREIGN KEY (id_conducteur) REFERENCES utilisateurs(id_utilisateur),
    FOREIGN KEY (id_passager) REFERENCES utilisateurs(id_utilisateur)
);

--Table messages (Messagerie intégrée)
CREATE TABLE messages (
    id_message INT PRIMARY KEY AUTO_INCREMENT,
    id_correspondance INT NOT NULL,
    id_expediteur INT NOT NULL,
    contenu TEXT NOT NULL,
    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    est_lu BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_correspondance) REFERENCES correspondances(id_correspondance),
    FOREIGN KEY (id_expediteur) REFERENCES utilisateurs(id_utilisateur)
);

--Table reinitialisations_mot_de_passe (Sécurité & récupération)
CREATE TABLE reinitialisation_mdp (
    id_reinitialisation INT PRIMARY KEY AUTO_INCREMENT,
    id_utilisateur INT NOT NULL,
    jeton VARCHAR(255) UNIQUE NOT NULL,
    expiration DATETIME NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur)
);


-- Index
CREATE INDEX idx_utilisateur_contact ON utilisateurs(email, telephone);
CREATE INDEX idx_matching_situation ON matching(situation, match_date);
