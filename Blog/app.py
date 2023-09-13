from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask import send_from_directory
from datetime import datetime
from models import db, Article, Evenement ,Education,Inscription,Admin, Contact
from flask_mail import Mail, Message

app = Flask(__name__, static_folder='stactic')

app.secret_key = 'simonsecret09'

# Configurez les paramètres de votre serveur SMTP (par exemple, Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'loryndacastle@gmail.com'  # Remplacez par votre adresse Gmail
app.config['MAIL_PASSWORD'] = 'Simon09@09'  # Remplacez par votre mot de passe Gmail

mail = Mail(app)


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Configuration de la base de données SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_base.db'  # Remplacez ceci par l'URL de votre base de données
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Associez l'application à la base de données
db.init_app(app)


#__vues__

@app.route('/')
def home():
    evenements = Evenement.query.all()  # Récupérez tous les événements depuis la base de données
    return render_template('pages/home.html', evenements=evenements)


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/recherche')
def recherche():
    articles = Article.query.all()  # Récupérez tous les articles depuis la base de données

    return render_template('pages/recherche.html', articles=articles)

@app.route('/contact')
def contact():
    return render_template('pages/contact.html')

@app.route('/contacte', methods=['POST'])
def contacte():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # Créez un objet Message pour l'e-mail
        msg = Message('Nouveau message de contact', sender=email, recipients=['loryndacastle@gmail.com'])
        msg.body = f"Nom: {name}\nEmail: {email}\nTéléphone: {phone}\nMessage:\n{message}"

        try:
            # Envoyez l'e-mail
            mail.send(msg)
            flash('Votre message a été envoyé avec succès.', 'success')
        except Exception as e:
            flash(f'Erreur lors de l\'envoi du message : {str(e)}', 'danger')

        return redirect('/contact')

@app.route('/service')
def service():
    return render_template('pages/service.html')


@app.route('/education')
def education():
    educations = Education.query.all()  # Récupérez tous les articles depuis la base de données
    return render_template('pages/education.html',educations=educations)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()    
    app.run(debug=True, port=3000)
