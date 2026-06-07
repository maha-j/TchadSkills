#!/bin/bash

echo "🚀 Installation de TchadSkills..."

# 1. Installation des dépendances
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# 2. Préparation de la base de données
echo "🗄️ Préparation de la base de données..."
python manage.py makemigrations core
python manage.py migrate

# 3. Peuplement des données
echo "🌱 Ajout des données de démonstration..."
python seed_data.py

echo "✅ Installation terminée !"
echo "🚀 Pour lancer le site, utilisez : python manage.py runserver"
