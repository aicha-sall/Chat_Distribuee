# Utiliser une image Python officielle comme base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système pour MySQL
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer un répertoire pour les templates s'il n'existe pas
RUN mkdir -p templates

# Exposer le port de l'application
EXPOSE 5000

# Variables d'environnement
ENV PYTHONPATH=/app
ENV FLASK_APP=chat_app.py

# Commande pour lancer l'application avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "chat_app:app"]
