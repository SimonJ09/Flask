#!/bin/bash
python -m venv Flaskapp
.\Flaskapp\Scripts\activate
python.exe -m pip install --upgrade pip
pip install --upgrade pip
gunicorn -c gunicorn_config.py app:app