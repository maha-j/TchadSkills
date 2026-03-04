# TchadSkills - Documentation Complète
## Plateforme E-Learning pour le Tchad

### 📋 Table des Matières
1. [Vue d'ensemble](#vue-densemble)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Fonctionnalités](#fonctionnalités)
6. [API Documentation](#api-documentation)
7. [Intégration Mobile Money](#intégration-mobile-money)
8. [Déploiement](#déploiement)
9. [Maintenance](#maintenance)

---

## 🎯 Vue d'ensemble

TchadSkills est une plateforme e-learning complète conçue spécifiquement pour le marché tchadien, offrant :

- **Formation en ligne** dans diverses catégories
- **Support multilingue** (Français et Arabe Tchadien)
- **Paiement Mobile Money** (Moov, Airtel, Tigo)
- **Certifications numériques** vérifiables
- **Forum communautaire** pour l'échange de connaissances

### Technologies Utilisées

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Responsive Design (Mobile-First)
- Progressive Web App (PWA) ready

**Backend:**
- Django 4.2 + Django REST Framework
- PostgreSQL / MySQL
- Celery pour les tâches asynchrones
- Redis pour le cache

**Infrastructure:**
- AWS S3 / Google Cloud Storage pour les médias
- Nginx + Gunicorn pour la production
- Docker pour la containerisation
- GitHub Actions pour CI/CD

---

## 🏗️ Architecture

### Architecture Globale

```
┌─────────────────────────────────────────────────┐
│              Frontend (HTML/CSS/JS)              │
│  - Interface utilisateur responsive              │
│  - PWA avec service workers                      │
│  - Optimisation mobile                           │
└──────────────────┬──────────────────────────────┘
                   │ REST API (JSON)
┌──────────────────▼──────────────────────────────┐
│           Backend API (Django REST)              │
│  - Authentification JWT                          │
│  - Gestion des cours et utilisateurs             │
│  - Intégration paiements                         │
└──────────────────┬──────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌────────┐  ┌──────────┐  ┌──────────┐
│Database│  │ Storage  │  │  Cache   │
│PostgreSQL│ │ AWS S3   │  │  Redis   │
└────────┘  └──────────┘  └──────────┘
```

### Structure de la Base de Données

**Tables Principales:**
- `users` - Utilisateurs (étudiants, formateurs, admins)
- `courses` - Cours et leurs métadonnées
- `course_sections` - Modules de cours
- `lessons` - Leçons individuelles
- `enrollments` - Inscriptions des étudiants
- `payments` - Transactions financières
- `certificates` - Certificats délivrés
- `reviews` - Évaluations de cours
- `forum_topics` & `forum_replies` - Forum communautaire

---

## 💻 Installation

### Prérequis

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Node.js 16+ (pour le build frontend si nécessaire)

### Installation Backend

```bash
# Cloner le repository
git clone https://github.com/votreorganisation/tchadskills.git
cd tchadskills

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos configurations

# Créer la base de données
createdb tchadskills

# Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Charger les données de test (optionnel)
python manage.py loaddata fixtures/initial_data.json

# Lancer le serveur de développement
python manage.py runserver
```

### Installation Frontend

Le frontend est déjà intégré dans `tchadskills.html`. Pour le déployer :

```bash
# Option 1: Serveur de développement simple
python -m http.server 8000

# Option 2: Nginx (production)
# Copier tchadskills.html dans /var/www/html/
sudo cp tchadskills.html /var/www/html/index.html
```

---

## ⚙️ Configuration

### Variables d'Environnement (.env)

```env
# Django
SECRET_KEY=votre-clé-secrète-très-longue-et-complexe
DEBUG=False
ALLOWED_HOSTS=tchadskills.td,www.tchadskills.td

# Database
DB_NAME=tchadskills
DB_USER=tchadskills_user
DB_PASSWORD=votre-mot-de-passe-sécurisé
DB_HOST=localhost
DB_PORT=5432

# AWS S3
AWS_ACCESS_KEY_ID=votre-access-key
AWS_SECRET_ACCESS_KEY=votre-secret-key
AWS_STORAGE_BUCKET_NAME=tchadskills-media
AWS_S3_REGION_NAME=eu-west-1

# Mobile Money
MOOV_MONEY_API_KEY=votre-clé-api-moov
MOOV_MONEY_SECRET=votre-secret-moov
AIRTEL_MONEY_API_KEY=votre-clé-api-airtel
AIRTEL_MONEY_SECRET=votre-secret-airtel
TIGO_CASH_API_KEY=votre-clé-api-tigo
TIGO_CASH_SECRET=votre-secret-tigo

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@tchadskills.td
EMAIL_HOST_PASSWORD=votre-mot-de-passe-email

# Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security
CORS_ALLOWED_ORIGINS=https://tchadskills.td,https://www.tchadskills.td
```

---

## 🚀 Fonctionnalités

### 1. Gestion des Utilisateurs

**Types d'utilisateurs:**
- **Étudiants** - Accès aux cours, progression, certificats
- **Formateurs** - Création et gestion de cours
- **Administrateurs** - Gestion complète de la plateforme

**Fonctionnalités:**
- Inscription / Connexion (JWT Authentication)
- Profils personnalisables
- Vérification email/téléphone
- Réinitialisation de mot de passe

### 2. Catalogue de Cours

**Catégories:**
- Développement Web
- Marketing Digital
- Design Graphique
- Bureautique
- Entrepreneuriat
- Langues

**Fonctionnalités cours:**
- Recherche et filtrage avancés
- Prévisualisation gratuite
- Évaluations et avis
- Prix flexibles (FCFA)
- Réductions et coupons

### 3. Contenu Pédagogique

**Types de contenu:**
- Vidéos HD avec lecteur intégré
- Articles et documents PDF
- Quiz interactifs
- Exercices pratiques
- Sessions live (à venir)

**Progression:**
- Suivi automatique
- Marquage des leçons complétées
- Temps passé par leçon
- Statistiques détaillées

### 4. Système de Paiement

**Méthodes supportées:**
- Moov Money
- Airtel Money
- Tigo Cash
- Cartes bancaires (Visa, Mastercard)

**Workflow:**
```
1. Sélection du cours
2. Choix de la méthode de paiement
3. Validation du numéro de téléphone
4. Confirmation du paiement
5. Inscription automatique
6. Email de confirmation
```

### 5. Certificats

**Génération automatique:**
- À la fin d'un cours (100% complété)
- Numéro unique de vérification
- Téléchargement PDF
- Partage sur réseaux sociaux

**Vérification:**
- URL publique de vérification
- QR Code sur chaque certificat
- Registre public des certificats

### 6. Forum Communautaire

**Fonctionnalités:**
- Discussions par cours
- Questions/Réponses
- Recherche de sujets
- Notifications en temps réel
- Système de modération

---

## 📚 API Documentation

### Authentication

**Obtenir un token JWT:**

```http
POST /api/token/
Content-Type: application/json

{
  "username": "utilisateur@email.com",
  "password": "motdepasse123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Utiliser le token:**

```http
GET /api/courses/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Endpoints Principaux

#### Cours

```http
# Liste des cours
GET /api/courses/
Query params: ?category=web&level=beginner&search=vue

# Détail d'un cours
GET /api/courses/{slug}/

# S'inscrire à un cours
POST /api/courses/{slug}/enroll/
Authorization: Bearer {token}

# Évaluer un cours
POST /api/courses/{slug}/review/
Authorization: Bearer {token}
{
  "rating": 5,
  "review_text": "Excellent cours!"
}
```

#### Catégories

```http
# Liste des catégories
GET /api/categories/

# Cours d'une catégorie
GET /api/categories/{slug}/
```

#### Inscriptions

```http
# Mes inscriptions
GET /api/enrollments/
Authorization: Bearer {token}

# Détail d'une inscription
GET /api/enrollments/{id}/

# Mettre à jour la progression
POST /api/enrollments/{id}/update_progress/
{
  "progress": 75.5
}
```

#### Paiements

```http
# Mes paiements
GET /api/payments/
Authorization: Bearer {token}

# Créer un paiement
POST /api/payments/
{
  "course_id": 1,
  "amount": 35000,
  "payment_method": "moov",
  "phone_number": "+23577123456"
}
```

#### Certificats

```http
# Mes certificats
GET /api/certificates/
Authorization: Bearer {token}

# Vérifier un certificat
GET /api/certificates/{id}/verify/
```

---

## 💳 Intégration Mobile Money

### Configuration Moov Money

```python
# settings.py
MOOV_MONEY_CONFIG = {
    'api_url': 'https://api.moov.td/v1',
    'merchant_id': 'VOTRE_MERCHANT_ID',
    'api_key': config('MOOV_MONEY_API_KEY'),
    'api_secret': config('MOOV_MONEY_SECRET'),
}
```

### Exemple d'intégration

```python
# payments/services.py
import requests
from django.conf import settings

def process_moov_payment(phone_number, amount, reference):
    """
    Traiter un paiement Moov Money
    """
    url = f"{settings.MOOV_MONEY_CONFIG['api_url']}/payments"
    
    headers = {
        'Authorization': f"Bearer {get_moov_token()}",
        'Content-Type': 'application/json'
    }
    
    data = {
        'merchant_id': settings.MOOV_MONEY_CONFIG['merchant_id'],
        'phone_number': phone_number,
        'amount': amount,
        'currency': 'XAF',
        'reference': reference,
        'description': 'Paiement cours TchadSkills'
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return {
            'success': True,
            'transaction_id': response.json()['transaction_id']
        }
    else:
        return {
            'success': False,
            'error': response.json().get('message', 'Erreur inconnue')
        }

def verify_moov_payment(transaction_id):
    """
    Vérifier le statut d'un paiement
    """
    url = f"{settings.MOOV_MONEY_CONFIG['api_url']}/payments/{transaction_id}"
    
    headers = {
        'Authorization': f"Bearer {get_moov_token()}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'status': data['status'],  # pending, completed, failed
            'amount': data['amount']
        }
    
    return None
```

### Webhooks pour les notifications

```python
# payments/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def moov_webhook(request):
    """
    Webhook pour recevoir les notifications Moov Money
    """
    # Vérifier la signature
    signature = request.headers.get('X-Moov-Signature')
    if not verify_webhook_signature(request.body, signature):
        return Response({'error': 'Invalid signature'}, status=401)
    
    data = request.data
    transaction_id = data['transaction_id']
    status = data['status']
    
    # Mettre à jour le paiement
    payment = Payment.objects.get(transaction_id=transaction_id)
    payment.payment_status = status
    payment.save()
    
    # Si paiement réussi, créer l'inscription
    if status == 'completed':
        Enrollment.objects.create(
            user=payment.user,
            course=payment.course
        )
        
        # Envoyer email de confirmation
        send_enrollment_confirmation_email(payment.user, payment.course)
    
    return Response({'status': 'ok'})
```

---

## 🌐 Déploiement

### Option 1: Déploiement sur VPS (Ubuntu 22.04)

```bash
# Installer les dépendances
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql redis-server

# Configurer PostgreSQL
sudo -u postgres createuser tchadskills
sudo -u postgres createdb tchadskills
sudo -u postgres psql -c "ALTER USER tchadskills WITH PASSWORD 'votremotdepasse';"

# Cloner et configurer l'application
cd /var/www
sudo git clone https://github.com/votreorganisation/tchadskills.git
cd tchadskills
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurer les variables d'environnement
sudo nano .env
# (Remplir les variables)

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Configurer Gunicorn
sudo nano /etc/systemd/system/tchadskills.service
```

**Fichier tchadskills.service:**

```ini
[Unit]
Description=TchadSkills Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/tchadskills
Environment="PATH=/var/www/tchadskills/venv/bin"
ExecStart=/var/www/tchadskills/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/tchadskills/tchadskills.sock \
          tchadskills.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Configuration Nginx:**

```nginx
# /etc/nginx/sites-available/tchadskills
server {
    listen 80;
    server_name tchadskills.td www.tchadskills.td;
    
    location / {
        root /var/www/tchadskills/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        include proxy_params;
        proxy_pass http://unix:/var/www/tchadskills/tchadskills.sock;
    }
    
    location /static {
        alias /var/www/tchadskills/staticfiles;
    }
    
    location /media {
        alias /var/www/tchadskills/media;
    }
}
```

**Activer et démarrer:**

```bash
# Activer le service
sudo systemctl start tchadskills
sudo systemctl enable tchadskills

# Configurer Nginx
sudo ln -s /etc/nginx/sites-available/tchadskills /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Configurer SSL avec Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tchadskills.td -d www.tchadskills.td
```

### Option 2: Déploiement avec Docker

**Dockerfile:**

```dockerfile
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tchadskills.wsgi:application"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=tchadskills
      - POSTGRES_USER=tchadskills
      - POSTGRES_PASSWORD=votremotdepasse

  redis:
    image: redis:6-alpine

  web:
    build: .
    command: gunicorn tchadskills.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

**Déployer:**

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🔧 Maintenance

### Sauvegardes

**Script de sauvegarde automatique:**

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/tchadskills"

# Sauvegarde de la base de données
pg_dump tchadskills > "$BACKUP_DIR/db_$DATE.sql"

# Sauvegarde des fichiers media
tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" /var/www/tchadskills/media

# Nettoyer les sauvegardes de plus de 30 jours
find $BACKUP_DIR -type f -mtime +30 -delete

# Envoyer vers S3 (optionnel)
aws s3 cp "$BACKUP_DIR/db_$DATE.sql" s3://tchadskills-backups/
```

**Crontab:**

```cron
# Sauvegarde quotidienne à 2h du matin
0 2 * * * /var/www/tchadskills/backup.sh
```

### Monitoring

**Logs à surveiller:**

```bash
# Logs Django
tail -f /var/www/tchadskills/logs/django.log

# Logs Nginx
tail -f /var/log/nginx/tchadskills-access.log
tail -f /var/log/nginx/tchadskills-error.log

# Logs système
journalctl -u tchadskills -f
```

### Mise à jour

```bash
# Arrêter les services
sudo systemctl stop tchadskills

# Mettre à jour le code
cd /var/www/tchadskills
git pull origin main

# Activer l'environnement virtuel
source venv/bin/activate

# Mettre à jour les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Redémarrer les services
sudo systemctl start tchadskills
sudo systemctl restart nginx
```

---

## 📊 Métriques de Performance

### Objectifs de Performance
- Temps de chargement initial : < 3 secondes
- Time to Interactive : < 5 secondes
- Score Lighthouse : > 90/100
- Disponibilité : 99.9%

### Optimisations
- Compression Gzip/Brotli
- Mise en cache Redis
- CDN pour les assets statiques
- Lazy loading des images et vidéos
- Minification CSS/JS

---

## 🤝 Support et Contact

**Documentation:** https://docs.tchadskills.td
**Email:** support@tchadskills.td
**Téléphone:** +235 XX XX XX XX
**Forum:** https://forum.tchadskills.td

---

## 📄 Licence

Copyright © 2026 TchadSkills. Tous droits réservés.

---

*Cette plateforme a été développée pour démocratiser l'accès à l'éducation au Tchad.* 🇹🇩
