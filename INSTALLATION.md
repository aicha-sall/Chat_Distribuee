# Guide d'Installation - Chat Distribué DEVNET

## 📋 Prérequis

1. **Docker Desktop** installé et en cours d'exécution
2. **Docker Compose** (inclus avec Docker Desktop)
3. **Git** pour cloner le repository
4. **Compte Docker Hub** pour le déploiement

## 🚀 Installation Rapide

### 1. Cloner le projet
```bash
git clone https://github.com/aicha-sall/Chat-.git
cd Chat-
```

### 2. Lancer les services
```bash
# Construire et démarrer tous les conteneurs
docker-compose up -d

# Vérifier l'état des services
docker-compose ps
```

### 3. Accéder à l'application
- **Service 1** : http://localhost:5000
- **Service 2** : http://localhost:5001
- **Base de données** : localhost:3306

## 📊 Démonstration du Chat

### Scénario de Test Complet

1. **Ouvrir deux navigateurs** :
   - Navigateur 1 : http://localhost:5000
   - Navigateur 2 : http://localhost:5001

2. **Créer des utilisateurs** :
   - Service 1 : Créer "Alice"
   - Service 2 : Créer "Bob"

3. **Tester la communication** :
   - Alice envoie un message depuis le service 1
   - Bob reçoit le message en temps réel sur le service 2
   - Bob répond depuis le service 2
   - Alice reçoit la réponse sur le service 1

4. **Vérifier la synchronisation** :
   - Les messages apparaissent sur les deux services
   - L'historique est partagé via la base de données MySQL
   - Les statistiques s'actualisent en temps réel

## 🔧 Configuration

### Variables d'Environnement
Le fichier `.env` contient :
```bash
DATABASE_URL=mysql+pymysql://chatuser:password@db:3306/chatdb
SERVICE_NAME=chat_service_1
SERVICE_PORT=5000
OTHER_SERVICE_URL=http://chat_service_2:5001
```

### Personnalisation
Pour modifier la configuration :
1. Éditez le fichier `docker-compose.yml`
2. Modifiez les variables d'environnement
3. Redémarrez avec `docker-compose restart`

## 🌐 Architecture Réseau

### Configuration des Services
- **Service 1** : `chat_service_1` (Port 5000)
- **Service 2** : `chat_service_2` (Port 5001)
- **Base de données** : `chat_mysql_db` (Port 3306)

### Réseau Docker
- **Nom** : `chat_network`
- **Subnet** : `172.21.0.0/16`
- **Communication** : Tous les services peuvent communiquer entre eux

## 📱 Fonctionnalités du Chat

### Interface Utilisateur
- **Création d'utilisateurs** : Chaque service peut créer des utilisateurs
- **Envoi de messages** : Communication en temps réel entre services
- **Historique partagé** : Tous les messages sont stockés dans MySQL
- **Statistiques en temps réel** : Nombre de messages et d'utilisateurs

### API Endpoints
- `GET /api/messages` : Récupérer tous les messages
- `POST /api/messages` : Envoyer un message
- `GET /api/users` : Lister les utilisateurs
- `POST /api/users` : Créer un utilisateur
- `GET /api/services` : État des services
- `GET /api/health` : Santé du service
- `GET /api/stats` : Statistiques du chat

## 🛠️ Commandes Utiles

### Gestion des Conteneurs
```bash
# Démarrer les services
docker-compose up -d

# Arrêter les services
docker-compose down

# Redémarrer les services
docker-compose restart

# Voir les logs en temps réel
docker-compose logs -f

# Supprimer tout (y compris les données)
docker-compose down -v
```

### Accès à la Base de Données
```bash
# Se connecter à MySQL
docker exec -it chat_mysql_db mysql -u chatuser -p chatdb

# Lister les tables
SHOW TABLES;

# Voir les messages
SELECT * FROM messages ORDER BY created_at DESC LIMIT 10;

# Voir les utilisateurs
SELECT * FROM users;
```

### Monitoring des Services
```bash
# État des conteneurs
docker-compose ps

# Utilisation des ressources
docker stats

# Logs d'un service spécifique
docker-compose logs chat1
docker-compose logs chat2
```

## 🚨 Dépannage

### Problèmes Courants

#### 1. "Port already in use"
```bash
# Vérifier quel processus utilise le port
netstat -ano | findstr :5000

# Arrêter le processus ou changer le port dans docker-compose.yml
```

#### 2. "Database connection failed"
```bash
# Vérifier que le conteneur de base de données est démarré
docker-compose ps db

# Redémarrer la base de données
docker-compose restart db

# Attendre 30 secondes pour l'initialisation
docker-compose up -d
```

#### 3. "Service communication failed"
```bash
# Vérifier le réseau Docker
docker network ls
docker network inspect chat_chat_network

# Redémarrer les services de chat
docker-compose restart chat1 chat2
```

#### 4. Docker Desktop non démarré
- Démarrez Docker Desktop manuellement
- Attendez que l'icône soit verte
- Vérifiez que la virtualisation est activée

### Logs Détaillés
```bash
# Logs de tous les services
docker-compose logs

# Logs avec timestamps
docker-compose logs -t

# Logs des 100 dernières lignes
docker-compose logs --tail=100
```

## 🐳 Déploiement sur Docker Hub

### Configuration GitHub Secrets
1. Allez dans votre repository GitHub
2. Settings → Secrets and variables → Actions
3. Ajoutez :
   - `DOCKER_USERNAME` : Votre nom d'utilisateur Docker Hub
   - `DOCKER_PASSWORD` : Votre mot de passe ou token Docker Hub

### Pipeline CI/CD
Le pipeline se déclenche automatiquement :
- À chaque push sur la branche `main`
- Construction de l'image Docker
- Publication sur Docker Hub : `aichasall/chat-distribue-devnet`

### Manuel
```bash
# Construire l'image localement
docker build -t aichasall/chat-distribue-devnet .

# Pousser sur Docker Hub
docker push aichasall/chat-distribue-devnet
```

## 📈 Performance et Scalabilité

### Monitoring
```bash
# Utilisation CPU/mémoire
docker stats

# Espace disque utilisé
docker system df

# Nettoyer les images inutilisées
docker system prune -a
```

### Scalabilité
Pour ajouter une troisième instance :
```yaml
# Ajouter dans docker-compose.yml
chat3:
  build: .
  ports:
    - "5002:5000"
  environment:
    DATABASE_URL: mysql+pymysql://chatuser:password@db:3306/chatdb
    SERVICE_NAME: chat_service_3
    SERVICE_PORT: "5002"
    OTHER_SERVICE_URL: http://chat_service_1:5000
```

## 🔒 Sécurité

### Mots de passe
Changez les mots de passe par défaut dans `docker-compose.yml` :
```yaml
environment:
  MYSQL_PASSWORD: votre_mot_de_passe_securise
  MYSQL_ROOT_PASSWORD: votre_root_password_securise
```

### Réseau
Le réseau Docker est isolé de l'hôte par défaut. Seuls les ports explicitement exposés sont accessibles.

## 📚 Documentation Complémentaire

- **Support de présentation** : `PRESENTATION.md`
- **README du projet** : `README.md`
- **Code source** : `chat_app.py`
- **Template HTML** : `templates/chat.html`

---

## Support Technique

En cas de problème :
1. Vérifiez les logs avec `docker-compose logs`
2. Consultez ce guide de dépannage
3. Redémarrez les services avec `docker-compose restart`

**Le chat distribué est maintenant prêt pour votre présentation DEVNET ! 🎉**
