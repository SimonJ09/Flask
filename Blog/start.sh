#!/bin/bash
python -m venv Flaskapp
.\Flaskapp\Scripts\activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
gunicorn -c gunicorn_config.py app:app