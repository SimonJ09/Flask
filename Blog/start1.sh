#!/bin/bash
python -m venv Flaskapp
.\Flaskapp\Scripts\activate
pip install --upgrade pip
gunicorn -c gunicorn_config.py app:app