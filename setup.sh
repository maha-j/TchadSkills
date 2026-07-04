#!/bin/bash
set -e

echo "🚀 Installation de TchadSkills..."

# 1. Installation des dépendances
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# 2. Préparation de la base de données
echo "🗄️ Préparation de la base de données..."
python manage.py migrate --noinput

# 3. Fichiers statiques pour la production
echo "🎨 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# 4. Peuplement des données
echo "🌱 Ajout des données de démonstration..."
python seed_data.py

echo "✅ Installation terminée !"
echo "🚀 Pour lancer le site, utilisez : python manage.py runserver"
