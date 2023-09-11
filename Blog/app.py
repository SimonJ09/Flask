from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask import send_from_directory
from datetime import datetime
from models import db, Utilisateur, Article, Evenement

app = Flask(__name__, static_folder='stactic')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Configuration de la base de données SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Remplacez ceci par l'URL de votre base de données
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Associez l'application à la base de données
db.init_app(app)


#__Admin__
###  Articles Admin
@app.route('/ajouter_article', methods=['POST'])
def ajouter_article():
    if request.method == 'POST':
        title = request.form['title']
        contenu = request.form['contenu']
        photo = request.form['photo']
        pdf = request.form['pdf']

        nouvel_article = Article(title=title, contenu=contenu, photo=photo, pdf=pdf)

        try:
            db.session.add(nouvel_article)
            db.session.commit()
            return redirect(url_for('liste_articles'))
        except:
            db.session.rollback()
            return "Une erreur s'est produite lors de l'ajout de l'article."

# Route pour afficher la liste des articles (Read)
@app.route('/articles')
def liste_articles():
    articles = Article.query.all()
    return render_template('liste_articles.html', articles=articles)

# Route pour afficher un article spécifique (Read)
@app.route('/article/<int:id>')
def voir_article(id):
    article = Article.query.get(id)
    return render_template('voir_article.html', article=article)

# Route pour mettre à jour un article (Update)
@app.route('/modifier_article/<int:id>', methods=['POST', 'GET'])
def modifier_article(id):
    article = Article.query.get(id)

    if request.method == 'POST':
        article.title = request.form['title']
        article.contenu = request.form['contenu']
        article.photo = request.form['photo']
        article.pdf = request.form['pdf']

        try:
            db.session.commit()
            return redirect(url_for('liste_articles'))
        except:
            db.session.rollback()
            return "Une erreur s'est produite lors de la mise à jour de l'article."

    return render_template('modifier_article.html', article=article)

# Route pour supprimer un article (Delete)
@app.route('/supprimer_article/<int:id>', methods=['POST'])
def supprimer_article(id):
    article = Article.query.get(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for('liste_articles'))
    except:
        db.session.rollback()
        return "Une erreur s'est produite lors de la suppression de l'article"
    
### evenements admin
@app.route('/ajouter_evenement', methods=['POST'])
def ajouter_evenement():
    if request.method == 'POST':
        title = request.form['title']
        contenu = request.form['contenu']
        photo = request.form['photo']
        pdf = request.form['pdf']

        nouvel_evenement = Evenement(title=title, contenu=contenu, photo=photo, pdf=pdf)

        db.session.add(nouvel_evenement)
        db.session.commit()

        return "L'événement a été ajouté avec succès."

@app.route('/evenement/<int:id>')
def voir_evenement(id):
    evenement = Evenement.query.get(id)
    return render_template('evenement.html', evenement=evenement)


@app.route('/modifier_evenement/<int:id>', methods=['POST', 'GET'])
def modifier_evenement(id):
    evenement = Evenement.query.get(id)

    if request.method == 'POST':
        evenement.title = request.form['title']
        evenement.contenu = request.form['contenu']
        evenement.photo = request.form['photo']
        evenement.pdf = request.form['pdf']

        db.session.commit()
        return "L'événement a été mis à jour avec succès."

    return render_template('modifier_evenement.html', evenement=evenement)

@app.route('/supprimer_evenement/<int:id>', methods=['POST'])
def supprimer_evenement(id):
    evenement = Evenement.query.get(id)
    db.session.delete(evenement)
    db.session.commit()
    return "L'événement a été supprimé avec succès."

### inscriptions admin

@app.route('/ajouter_inscription', methods=['POST'])
def ajouter_inscription():
    if request.method == 'POST':
        Nom = request.form['Nom']
        Prenom = request.form['Prenom']
        email = request.form['email']
        telephone = request.form['telephone']
        adresse = request.form['adresse']
        date_de_naissance = request.form['date_de_naissance']
        titre = request.form['titre']

        nouvelle_inscription = Inscription(Nom=Nom, Prenom=Prenom, email=email, 
                                           telephone=telephone, adresse=adresse,
                                           date_de_naissance=date_de_naissance, titre=titre)

        db.session.add(nouvelle_inscription)
        db.session.commit()

        return "L'inscription a été ajoutée avec succès."


@app.route('/inscription/<int:id>')
def voir_inscription(id):
    inscription = Inscription.query.get(id)
    return render_template('inscription.html', inscription=inscription)


@app.route('/modifier_inscription/<int:id>', methods=['POST', 'GET'])
def modifier_inscription(id):
    inscription = Inscription.query.get(id)

    if request.method == 'POST':
        inscription.Nom = request.form['Nom']
        inscription.Prenom = request.form['Prenom']
        inscription.email = request.form['email']
        inscription.telephone = request.form['telephone']
        inscription.adresse = request.form['adresse']
        inscription.date_de_naissance = request.form['date_de_naissance']
        inscription.titre = request.form['titre']

        db.session.commit()
        return "L'inscription a été mise à jour avec succès."

    return render_template('modifier_inscription.html', inscription=inscription)


@app.route('/supprimer_inscription/<int:id>', methods=['POST'])
def supprimer_inscription(id):
    inscription = Inscription.query.get(id)
    db.session.delete(inscription)
    db.session.commit()
    return "L'inscription a été supprimée avec succès."

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifiez les informations d'identification de l'administrateur ici
        if username == 'admin' and password == 'mot_de_passe':
            # Les informations d'identification sont valides, redirigez l'administrateur vers la page d'administration
            return redirect(url_for('page_admin'))

    return render_template('connexion.html')

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


@app.route('/service')
def service():
    return render_template('pages/service.html')


@app.route('/education')
def education():
    return render_template('pages/education.html')

# Configuration pour l'envoi d'e-mails
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'votre_email@gmail.com'
SMTP_PASSWORD = 'votre_mot_de_passe'
ADMIN_EMAIL = 'admin@example.com'  # Adresse e-mail de l'administrateur

@app.route('/envoyer_message', methods=['POST'])
def envoyer_message():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        telephone = request.form['telephone']
        message = request.form['message']

        # Configuration de l'e-mail
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = ADMIN_EMAIL  # L'adresse e-mail de l'administrateur
        msg['Subject'] = 'Nouveau message de contact'

        # Corps de l'e-mail
        texte = f"Nom: {nom}\nEmail: {email}\nTéléphone: {telephone}\n\nMessage:\n{message}"
        msg.attach(MIMEText(texte, 'plain'))

        # Connexion au serveur SMTP de Gmail et envoi de l'e-mail
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, ADMIN_EMAIL, msg.as_string())
            server.quit()
            return "Message envoyé avec succès à l'administrateur!"
        except Exception as e:
            return f"Une erreur s'est produite lors de l'envoi du message : {str(e)}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()    
    app.run(debug=True, port=3000)
