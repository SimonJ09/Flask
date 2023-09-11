from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255))
    mot_de_passe = db.Column(db.String(255))

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    contenu = db.Column(db.Text)
    photo = db.Column(db.String(255))
    pdf = db.Column(db.String(255))

class Evenement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    contenu = db.Column(db.Text)
    photo = db.Column(db.String(255))
    pdf = db.Column(db.String(255))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255))
    email = db.Column(db.String(255))
    message = db.Column(db.Text)

class Inscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(255))
    Prenom = db.Column(db.String(255))
    email = db.Column(db.String(255))
    telephone = db.Column(db.String(20))  # Assuming the phone number can be a string
    adresse = db.Column(db.String(255))
    date_de_naissance = db.Column(db.Date)  # Assuming date of birth is stored as a Date
    titre = db.Column(db.String(255))

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    programme = db.Column(db.String(255), nullable=False)
    nom = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(255), nullable=True)
    photho = db.Column(db.String(255), nullable=True)  # Vérifiez si vous vouliez avoir deux champs distincts photo et photho
    pdf = db.Column(db.String(255), nullable=True)