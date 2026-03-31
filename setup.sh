#!/bin/bash

echo "🚀 Configuration du Chat Distribué DEVNET"

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

# Créer les répertoires nécessaires
mkdir -p templates
mkdir -p .github/workflows

# Construire et lancer les conteneurs
echo "🔨 Construction des images Docker..."
docker-compose build

echo "💬 Démarrage des services de chat..."
docker-compose up -d

# Attendre que la base de données soit prête
echo "⏳ Attente de la base de données MySQL..."
sleep 15

# Vérifier que tout fonctionne
echo "✅ Vérification des services..."
docker-compose ps

echo ""
echo "🎉 Installation terminée!"
echo ""
echo "💬 Accès au chat distribué:"
echo "   Service 1: http://localhost:5000"
echo "   Service 2: http://localhost:5001"
echo ""
echo "🗄️ Base de données MySQL:"
echo "   Host: localhost:3306"
echo "   Database: chatdb"
echo "   User: chatuser"
echo "   Password: password"
echo ""
echo "🔧 Commandes utiles:"
echo "   Voir les logs: docker-compose logs -f"
echo "   Arrêter: docker-compose down"
echo "   Redémarrer: docker-compose restart"
echo ""
echo "🌐 Pour tester la communication:"
echo "   1. Ouvrez http://localhost:5000 dans un navigateur"
echo "   2. Ouvrez http://localhost:5001 dans un autre navigateur"
echo "   3. Créez des utilisateurs sur chaque service"
echo "   4. Envoyez des messages entre les services"
echo ""
echo "🐳 Pour Docker Hub:"
echo "   Image: aichasall/chat-distribue-devnet"
echo "   CI/CD: GitHub Actions configuré"
