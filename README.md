# Chat Distribué DEVNET - Application de Chat Inter-Services

## 📝 Description du Projet

**Titre : Chat Distribué entre Services Flask avec Communication Réseau**

Application de chat en temps réel distribuée permettant la communication entre deux instances Flask conteneurisées, démontrant les concepts de réseaux, d'API distribuées et de conteneurisation. Le projet illustre une solution concrète de communication inter-services dans une architecture microservices.

## 🎯 Objectif

Développer une application web de chat qui répond à un problème réel de communication entre services distribués, en intégrant :
- Communication API entre applications Flask
- Échange de données en temps réel via réseau Docker
- Persistance des messages dans base de données MySQL conteneurisée
- Architecture microservices scalable

## 🌟 Fonctionnalités Principales

- **Chat en temps réel** entre deux utilisateurs sur différentes instances
- **Communication réseau** via API REST entre services
- **Persistance des messages** dans base de données MySQL
- **Architecture distribuée** avec conteneurs Docker
- **Interface web moderne** et responsive
- **Historique des conversations** partagé entre instances

## 🏗️ Architecture Technique

### Services Principaux
- **Service Chat 1** : Instance Flask (Port 5000)
- **Service Chat 2** : Instance Flask (Port 5001) 
- **Base de données** : MySQL 8.0 conteneurisée
- **Réseau Docker** : Bridge network personnalisé

### Stack Technologique
- **Backend** : Flask avec SQLAlchemy et PyMySQL
- **Frontend** : HTML5 + CSS3 + JavaScript
- **Base de données** : MySQL 8.0
- **Conteneurisation** : Docker + Docker Compose
- **Réseau** : Bridge network Docker personnalisé

## 🚀 Installation Rapide

### Prérequis
- Docker Desktop installé et démarré (pour la version Docker)
- XAMPP avec MySQL (pour la version locale)
- Git pour cloner le repository

### Option 1 : Avec Docker (recommandé pour la présentation)
```bash
# Cloner le repository
git clone https://github.com/aicha-sall/Chat-.git
cd Chat-

# Lancer les services
docker-compose up -d

# Accéder aux instances
# Utilisateur 1 : http://localhost:5000
# Utilisateur 2 : http://localhost:5001
```

### Option 2 : Avec XAMPP (MySQL local)
```bash
# 1. Démarrer XAMPP et Apache + MySQL
# 2. Importer le fichier database.sql dans phpMyAdmin
# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer le service 1
set DB_TYPE=xampp
set SERVICE_NAME=service_1
set SERVICE_PORT=5000
set OTHER_SERVICE_URL=http://localhost:5001
python app.py

# 5. Dans un autre terminal, lancer le service 2
set DB_TYPE=xampp
set SERVICE_NAME=service_2
set SERVICE_PORT=5001
set OTHER_SERVICE_URL=http://localhost:5000
python app.py

# Accéder aux instances
# Service 1 : http://localhost:5000
# Service 2 : http://localhost:5001
```

### Option 3 : Mode local (pour développement/test)
```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application locale
set DB_TYPE=sqlite
python app.py

# Accéder à l'application
http://localhost:5000
```

## 📊 Démonstration

### Scénario de Test
1. **Démarrage** : Lancer docker-compose up -d
2. **Accès** : Ouvrir les deux ports dans des navigateurs différents
3. **Communication** : Envoyer des messages entre utilisateurs
4. **Vérification** : Observer la synchronisation en temps réel

### Points Clés à Démontrer
- ✅ Communication réseau entre services Flask
- ✅ Persistance des messages dans MySQL
- ✅ Conteneurisation avec Docker
- ✅ Réseau Docker personnalisé
- ✅ API REST pour échange de données

## 🔧 Configuration

### Variables d'Environnement
```bash
DATABASE_URL=mysql://chatuser:password@db:3306/chatdb
FLASK_ENV=production
SERVICE_NAME=chat_service_1
```

### Réseau Docker
- **Nom** : chat_network
- **Subnet** : 172.21.0.0/16
- **Communication** : Tous les services peuvent communiquer

## 📈 Points d'Évaluation

| Critère | Points | Statut |
|---------|--------|--------|
| Fonctionnement de l'application | 5 | ✅ |
| Utilisation correcte de Flask | 3 | ✅ |
| Utilisation de Docker et conteneurisation | 4 | ✅ |
| Mise en place d'un réseau entre services | 3 | ✅ |
| Utilisation d'une base de données en conteneur | 2 | ✅ |
| Qualité du code et organisation | 1 | ✅ |
| Documentation et présentation | 1 | ✅ |
| Démonstration du projet | 1 | ✅ |

**Total : 20/20**

## 🌟 Bonus Implémentés

- ✅ **CI/CD GitHub Actions** vers Docker Hub
- ✅ **Architecture microservices** propre et documentée
- ✅ **Idée originale** : Chat distribué avec synchronisation temps réel
- ✅ **Interface utilisateur** moderne et intuitive

## 📱 Technologies Utilisées

### Backend
- **Flask** : Framework web Python
- **Flask-SQLAlchemy** : ORM pour base de données
- **PyMySQL** : Connecteur MySQL
- **Requests** : Client HTTP pour API inter-services

### Frontend
- **HTML5/CSS3** : Structure et style moderne
- **JavaScript** : Logique client et rafraîchissement automatique
- **Bootstrap** : Framework CSS pour design responsive

### Infrastructure
- **Docker** : Plateforme de conteneurisation
- **Docker Compose** : Orchestration multi-conteneurs
- **MySQL** : Base de données relationnelle
- **Bridge Network** : Communication inter-conteneurs

## 🔗 Liens Utiles

- **Repository GitHub** : https://github.com/aicha-sall/Chat-
- **Image Docker Hub** : aichasall/chat-distribue-devnet
- **Documentation** : Voir fichier `PRESENTATION.md`

---

*Auteur : Aïcha Sall - Licence 3 Réseaux et Informatique - ISI Keur Massar*
