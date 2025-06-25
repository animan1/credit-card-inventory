# Makefile for credit-card-inventory Django project

VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
DJANGO_MANAGE := $(PYTHON) manage.py

.PHONY: help quickstart venv install migrate makemigrations run createsuperuser shell clean venv-shell

help:
	@echo "Usage:"
	@echo "  make quickstart       - Full project bootstrap"
	@echo "  make venv             - Create virtual environment"
	@echo "  make install          - Install Python dependencies"
	@echo "  make migrate          - Apply database migrations"
	@echo "  make makemigrations   - Generate migrations from models"
	@echo "  make run              - Run development server"
	@echo "  make createsuperuser  - Create admin account"
	@echo "  make shell            - Launch Django shell"
	@echo "  make clean            - Delete venv + pycache"

quickstart: venv install migrate
	@echo "✔️  Project setup complete. You can now run 'make run' or 'make createsuperuser'."

venv:
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)

venv-shell:
	@echo "💡 Activating virtual environment shell (type 'exit' to leave)..."
	@bash -c 'source $(VENV_DIR)/bin/activate && exec bash'

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

migrate:
	$(DJANGO_MANAGE) migrate

makemigrations:
	$(DJANGO_MANAGE) makemigrations

run:
	$(DJANGO_MANAGE) runserver

createsuperuser:
	$(DJANGO_MANAGE) createsuperuser

shell:
	$(DJANGO_MANAGE) shell

clean:
	rm -rf $(VENV_DIR)
	find . -type d -name '__pycache__' -exec rm -r {} +
