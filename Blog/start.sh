#!/bin/bash
rm -r .venv  # Supprimer l'environnement virtuel existant
python -m venv .venv  # Recréer l'environnement virtuel
.venv\Scripts\activate


pip install --upgrade pip
pip install --upgrade -r requirements.txt
python app.py
