#!/bin/bash
python -m venv Flaskapp

# Activez l'environnement virtuel Flask
source Flaskapp/bin/activate
# Mise à jour de pip dans l'environnement virtuel
python -m pip install --upgrade pip

# Installez les dépendances de votre application Flask (vous devez spécifier le chemin complet)
pip install -r requirements.txt

# Lancement de l'application avec Gunicorn
gunicorn -c gunicorn_config.py app:app1
