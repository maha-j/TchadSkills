# Makefile pour TchadSkills
# Utilisez 'make' suivi d'une cible pour exécuter les commandes

.PHONY: help install setup migrate run test lint format clean deploy docker-up docker-down

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
MANAGE := $(PYTHON) manage.py

# Couleurs pour l'affichage
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help:
	@echo "$(BLUE)╔════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║          TchadSkills - Makefile Commands               ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Setup & Installation:$(NC)"
	@echo "  make install           - Installer les dépendances"
	@echo "  make setup             - Configuration initiale (install + migrate + seed)"
	@echo "  make venv              - Créer l'environnement virtuel"
	@echo ""
	@echo "$(GREEN)Database:$(NC)"
	@echo "  make migrate           - Appliquer les migrations"
	@echo "  make makemigrations    - Créer les migrations"
	@echo "  make migrations-show   - Afficher l'état des migrations"
	@echo "  make createsuperuser   - Créer un superutilisateur"
	@echo "  make seed              - Charger les données de test"
	@echo "  make reset-db          - Réinitialiser la base de données"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make run               - Lancer le serveur de développement"
	@echo "  make shell             - Django shell interactif"
	@echo "  make static            - Collecter les fichiers statiques"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  make test              - Exécuter tous les tests"
	@echo "  make test-coverage     - Tests avec rapport de couverture"
	@echo "  make test-verbose      - Tests avec mode verbose"
	@echo ""
	@echo "$(GREEN)Code Quality:$(NC)"
	@echo "  make lint              - Vérifier le code (flake8, pylint)"
	@echo "  make format            - Formater le code (black, isort)"
	@echo "  make check             - Vérifier les problèmes de code"
	@echo ""
	@echo "$(GREEN)Docker:$(NC)"
	@echo "  make docker-up         - Démarrer les conteneurs"
	@echo "  make docker-down       - Arrêter les conteneurs"
	@echo "  make docker-logs       - Afficher les logs"
	@echo "  make docker-build      - Construire les images"
	@echo ""
	@echo "$(GREEN)Deployment:$(NC)"
	@echo "  make deploy-dev        - Déployer sur développement"
	@echo "  make deploy-prod       - Déployer sur production"
	@echo "  make deploy-backup     - Faire une sauvegarde avant déploiement"
	@echo ""
	@echo "$(GREEN)Utilities:$(NC)"
	@echo "  make clean             - Nettoyer les fichiers temporaires"
	@echo "  make requirements      - Générer requirements.txt à jour"
	@echo ""

# ======================== Setup & Installation ========================

venv:
	@echo "$(BLUE)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)✓ Virtual environment created$(NC)"
	@echo "Activate it with: source $(VENV)/bin/activate"

install: venv
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

setup: install migrate createsuperuser seed
	@echo "$(GREEN)✓ Setup completed successfully!$(NC)"
	@echo "Run 'make run' to start the development server"

# ======================== Database Commands ========================

migrate:
	@echo "$(BLUE)Applying migrations...$(NC)"
	$(MANAGE) migrate
	@echo "$(GREEN)✓ Migrations applied$(NC)"

makemigrations:
	@echo "$(BLUE)Creating migrations...$(NC)"
	$(MANAGE) makemigrations
	@echo "$(GREEN)✓ Migrations created$(NC)"

migrations-show:
	@echo "$(BLUE)Migrations status:$(NC)"
	$(MANAGE) showmigrations

createsuperuser:
	@echo "$(BLUE)Creating superuser...$(NC)"
	$(MANAGE) createsuperuser

seed:
	@echo "$(BLUE)Loading fixture data...$(NC)"
	$(MANAGE) loaddata fixtures/initial_data.json
	@echo "$(GREEN)✓ Fixture data loaded$(NC)"

reset-db:
	@echo "$(RED)WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		find . -path "*/migrations/*.py" -not -name "__init__.py" -delete; \
		find . -path "*/migrations/*.pyc" -delete; \
		rm -f db.sqlite3; \
		$(MANAGE) makemigrations; \
		$(MANAGE) migrate; \
		$(MANAGE) createsuperuser; \
		echo "$(GREEN)✓ Database reset$(NC)"; \
	else \
		echo "Cancelled"; \
	fi

# ======================== Development Commands ========================

run:
	@echo "$(BLUE)Starting development server...$(NC)"
	@echo "$(GREEN)Server running at http://localhost:8000$(NC)"
	$(MANAGE) runserver

shell:
	@echo "$(BLUE)Opening Django shell...$(NC)"
	$(MANAGE) shell

static:
	@echo "$(BLUE)Collecting static files...$(NC)"
	$(MANAGE) collectstatic --noinput
	@echo "$(GREEN)✓ Static files collected$(NC)"

check:
	@echo "$(BLUE)Checking Django setup...$(NC)"
	$(MANAGE) check

# ======================== Testing Commands ========================

test:
	@echo "$(BLUE)Running tests...$(NC)"
	pytest

test-verbose:
	@echo "$(BLUE)Running tests (verbose)...$(NC)"
	pytest -v

test-coverage:
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest --cov=. --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/$(NC)"

test-fast:
	@echo "$(BLUE)Running tests (fast mode)...$(NC)"
	pytest --maxfail=1 -x

# ======================== Code Quality ========================

lint:
	@echo "$(BLUE)Linting with flake8...$(NC)"
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "$(BLUE)Checking with pylint...$(NC)"
	pylint apps/ --exit-zero
	@echo "$(GREEN)✓ Linting complete$(NC)"

format:
	@echo "$(BLUE)Formatting code with black...$(NC)"
	black .
	@echo "$(BLUE)Sorting imports with isort...$(NC)"
	isort .
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check:
	@echo "$(BLUE)Checking code format...$(NC)"
	black --check .
	isort --check-only .

security:
	@echo "$(BLUE)Running security checks...$(NC)"
	bandit -r . -ll
	safety check

# ======================== Docker Commands ========================

docker-up:
	@echo "$(BLUE)Starting Docker containers...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Containers started$(NC)"

docker-down:
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Containers stopped$(NC)"

docker-build:
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Images built$(NC)"

docker-logs:
	@echo "$(BLUE)Displaying Docker logs...$(NC)"
	docker-compose logs -f

docker-shell:
	@echo "$(BLUE)Opening container shell...$(NC)"
	docker-compose exec web bash

docker-migrate:
	@echo "$(BLUE)Running migrations in container...$(NC)"
	docker-compose exec web python manage.py migrate

# ======================== Deployment Commands ========================

deploy-backup:
	@echo "$(BLUE)Creating backup...$(NC)"
	bash scripts/backup.sh
	@echo "$(GREEN)✓ Backup created$(NC)"

deploy-dev: deploy-backup
	@echo "$(BLUE)Deploying to development...$(NC)"
	git push origin develop
	@echo "$(GREEN)✓ Deployed to development$(NC)"

deploy-prod: deploy-backup
	@echo "$(RED)Deploying to PRODUCTION!$(NC)"
	@read -p "Are you sure? (yes/no): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		git push origin main; \
		echo "$(GREEN)✓ Deployed to production$(NC)"; \
	else \
		echo "Cancelled"; \
	fi

# ======================== Utility Commands ========================

clean:
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

requirements:
	@echo "$(BLUE)Updating requirements.txt...$(NC)"
	pip freeze > requirements.txt
	@echo "$(GREEN)✓ requirements.txt updated$(NC)"

status:
	@echo "$(BLUE)Git status:$(NC)"
	git status
	@echo ""
	@echo "$(BLUE)Branches:$(NC)"
	git branch -a

log:
	@echo "$(BLUE)Recent commits:$(NC)"
	git log --oneline -10

# ======================== Git Commands ========================

git-setup:
	@echo "$(BLUE)Setting up Git...$(NC)"
	git config --local user.name "TchadSkills Developer"
	git config --local user.email "dev@tchadskills.td"
	git config --local core.editor "nano"
	@echo "$(GREEN)✓ Git configured$(NC)"

git-push:
	@echo "$(BLUE)Pushing to remote...$(NC)"
	git push origin $$(git rev-parse --abbrev-ref HEAD)

git-pull:
	@echo "$(BLUE)Pulling from remote...$(NC)"
	git pull origin $$(git rev-parse --abbrev-ref HEAD)

# ======================== All-in-one Commands ========================

all: clean lint format test
	@echo "$(GREEN)✓ All checks passed!$(NC)"

dev-ready: install migrate static
	@echo "$(GREEN)✓ Development environment ready!$(NC)"

prod-check: lint test security
	@echo "$(GREEN)✓ Production checks passed!$(NC)"

.DEFAULT_GOAL := help
