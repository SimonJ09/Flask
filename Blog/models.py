from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    contenu = db.Column(db.Text)
    photo = db.Column(db.String(255))
    pdf = db.Column(db.String(255))
    auteur = db.Column(db.String(255))  # Ajout du champ Auteur
    date_publication = db.Column(db.Date)  # Ajout du champ Date de publication

    def get_photo_path(self):
        # Remplacez 'nom_de_la_colonne_photo' par le nom de la colonne dans votre modèle
        return 'media/images/article/' + self.photo
    
    
    def get_pdf_path(self):
        # Remplacez 'nom_de_la_colonne_pdf' par le nom de la colonne dans votre modèle
        return 'media/pdfs/article/' + self.pdf


class Evenement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    contenu = db.Column(db.Text)
    photo = db.Column(db.String(255))
    pdf = db.Column(db.String(255))
    date_de_depart = db.Column(db.Date)  # Ajout du champ Date de départ
    date_de_fin = db.Column(db.Date)  # Ajout du champ Date de fin
    
    def get_photo_path(self):
        # Remplacez 'nom_de_la_colonne_photo' par le nom de la colonne dans votre modèle
        return 'media/images/evenement/' + self.photo
    
    
    def get_pdf_path(self):
        # Remplacez 'nom_de_la_colonne_pdf' par le nom de la colonne dans votre modèle
        return 'media/pdfs/evenement/' + self.pdf

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
    pdf = db.Column(db.String(255), nullable=True)
    duree = db.Column(db.String(50), nullable=True)  # Ajout du champ Durée
    date_debut = db.Column(db.Date, nullable=True)  # Ajout du champ Date de début

    def get_photo_path(self):
        # Remplacez 'nom_de_la_colonne_photo' par le nom de la colonne dans votre modèle
        return 'media/images/education/' + self.photo
    
    
    def get_pdf_path(self):
        # Remplacez 'nom_de_la_colonne_pdf' par le nom de la colonne dans votre modèle
        return 'media/pdfs/education/' + self.pdf
