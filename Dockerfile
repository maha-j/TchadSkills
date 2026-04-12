# Utiliser une image Python officielle légère
FROM python:3.11-slim

# Empêcher Python de générer des fichiers .pyc et assurer l'affichage des logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code du projet
COPY . /app/

# Collecter les fichiers statiques pour la production
RUN python manage.py collectstatic --noinput

# Exposer le port par défaut
EXPOSE 8000

# Commande de lancement avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tchadskills_project.wsgi:application"]
