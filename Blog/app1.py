from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask import send_from_directory
from flask import request
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import db, Article, Evenement ,Education,Inscription,Admin, Contact


app = Flask(__name__, static_folder='stactic')

app.secret_key = 'simonsecret09'


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


#__Admin__
###  Articles Admin

@app.route('/page_admin')
def page_admin():
    return render_template('Admin/page_admin.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        # Recherchez l'administrateur dans la base de données en fonction du nom d'utilisateur
        admin = Admin.query.filter_by(username=username).first()
    
        # Vérifiez si un administrateur avec le nom d'utilisateur donné existe et si le mot de passe correspond
        if admin and admin.password == password:
            return redirect(url_for('page_admin'))
    return render_template('Admin/login.html')

# Route pour afficher la liste des articles (Read)
@app.route('/articles')
def articles():
    articles = Article.query.all()
    return render_template('Admin/articles.html', articles=articles)


@app.route('/ajouter_article', methods=['POST'])
def ajouter_article():
    if request.method == 'POST':
        title = request.form['title']
        contenu = request.form['contenu']
        photo = request.files['photo']  # Accédez au fichier photo
        pdf = request.files['pdf']  # Accédez au fichier PDF
        auteur = request.form['auteur']
        date_publication_str = request.form['date_publication']
        date_publication = datetime.strptime(date_publication_str, '%Y-%m-%d').date()

        # Vérifiez si les fichiers ont été téléchargés
        if photo and pdf:
            # Assurez-vous que les noms de fichiers sont sécurisés pour éviter les problèmes de sécurité
            photo_filename = secure_filename(photo.filename)
            pdf_filename = secure_filename(pdf.filename)

            # Définissez le chemin où vous souhaitez stocker les fichiers
            photo_path = os.path.join('media/images/article/', photo_filename)
            pdf_path = os.path.join('media/pdfs/article/', pdf_filename)

            # Enregistrez les fichiers téléchargés
            photo.save(photo_path)
            pdf.save(pdf_path)

            # Maintenant, vous pouvez créer l'objet Article avec les chemins des fichiers
            nouvel_article = Article(
                title=title,
                contenu=contenu,
                photo=photo_path,
                pdf=pdf_path,
                auteur=auteur,
                date_publication=date_publication
            )
            try:
                db.session.add(nouvel_article)
                db.session.commit()
                return redirect(url_for('page_admin'))
            except Exception as e:
                db.session.rollback()
                error_message = str(e)  # Convertit l'exception en une chaîne de caractères
                return f"Erreur lors de l'ajout de l'article : {error_message}"

    # Si la méthode est GET ou si le formulaire n'a pas été soumis, affichez simplement le formulaire
    return render_template('Admin/articles.html')

@app.route('/ajout_article_form', methods=['GET', 'POST'])
def ajout_article_form():
    return render_template('Admin/ajout_form.html')

@app.route('/supprimer_article/<int:article_id>', methods=['GET', 'POST'])
def supprimer_article(article_id):
    if request.method == 'GET':
        article = Article.query.get(article_id)

        if article:
            try:
                # Supprimez l'objet Article de la base de données
                db.session.delete(article)
                db.session.commit()
                return redirect(url_for('page_admin'))
            except Exception as e:
                db.session.rollback()
                error_message = str(e)  # Convertit l'exception en une chaîne de caractères
                return f"Erreur lors de la suppression de l'article : {error_message}"

    # Si la méthode est GET ou si la suppression n'a pas réussi, redirigez simplement l'utilisateur
    return redirect(url_for('page_admin'))


@app.route('/editer_article/<int:article_id>', methods=['GET', 'POST'])
def editer_article(article_id):
    article = Article.query.get(article_id)

    if article:
        if request.method == 'POST':
            # Récupérez les données modifiées du formulaire
            new_title = request.form.get('new_title')
            new_contenu = request.form.get('new_contenu')
            new_auteur = request.form.get('new_auteur')
            new_date_publication_str = request.form.get('new_date_publication')
            new_date_publication = datetime.strptime(new_date_publication_str, '%Y-%m-%d').date()

            # Mettez à jour les informations de l'article
            article.title = new_title
            article.contenu = new_contenu
            article.auteur = new_auteur
            article.date_publication = new_date_publication

            try:
                db.session.commit()
                flash('L\'article a été modifié avec succès.', 'success')
                return redirect(url_for('page_admin'))
            except Exception as e:
                db.session.rollback()
                error_message = str(e)
                return f"Erreur lors de la modification de l'article : {error_message}"

        return render_template('Admin/edit_article.html', article=article)

    flash('L\'article n\'existe pas.', 'danger')
    return redirect(url_for('page_admin'))


### Admin 
# Route pour afficher la liste des articles (Read)
@app.route('/admins')
def admins():
    admins = Admin.query.all()
    return render_template('Admin/admins.html', admins=admins)


@app.route('/admin/add', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Vérifiez si l'administrateur existe déjà
        existing_admin = Admin.query.filter_by(username=username).first()
        if existing_admin:
            flash('Cet administrateur existe déjà.', 'danger')
        else:
            new_admin = Admin(username=username, password=password)
            db.session.add(new_admin)
            db.session.commit()  # N'oubliez pas de commettre les modifications
            flash('Nouvel administrateur ajouté avec succès.', 'success')
            return redirect(url_for('page_admin'))

    return render_template('Admin/ajout_admin.html')

@app.route('/admin/delete/<int:admin_id>', methods=['GET', 'POST'])
def delete_admin(admin_id):
    admin = Admin.query.get(admin_id)

    if admin:
        if request.method == 'POST':
            db.session.delete(admin)
            db.session.commit()
            flash('L\'administrateur a été supprimé avec succès.', 'success')
            return redirect(url_for('page_admin'))

        return render_template('Admin/confirm_delete.html', admin=admin)

    flash('L\'administrateur n\'existe pas.', 'danger')
    return redirect(url_for('page_admin'))

@app.route('/admin/edit/<int:admin_id>', methods=['GET', 'POST'])
def edit_admin(admin_id):
    admin = Admin.query.get(admin_id)

    if admin:
        if request.method == 'POST':
            new_username = request.form.get('new_username')
            new_password = request.form.get('new_password')

            # Mettez à jour les informations de l'administrateur
            admin.username = new_username
            admin.password = new_password

            db.session.commit()
            flash('Les informations de l\'administrateur ont été mises à jour avec succès.', 'success')
            return redirect(url_for('page_admin'))

        return render_template('Admin/edit_admin.html', admin=admin)

    flash('L\'administrateur n\'existe pas.', 'danger')
    return redirect(url_for('page_admin'))

### evenements

@app.route('/evenements')
def evenements():
    evenements = Evenement.query.all()
    return render_template('Admin/evenements.html', evenements=evenements)

@app.route('/ajouter_evenement', methods=['POST'])
def ajouter_evenement():
    if request.method == 'POST':
        title = request.form['title']
        contenu = request.form['contenu']
        photo = request.files['photo']  # Accédez au fichier photo
        pdf = request.files['pdf']  # Accédez au fichier PDF
        date_de_depart_str = request.form['date_de_depart']
        date_de_fin_str = request.form['date_de_fin']
        date_de_fin = datetime.strptime(date_de_fin_str, '%Y-%m-%d').date()
        date_de_depart = datetime.strptime(date_de_depart_str, '%Y-%m-%d').date()

        # Vérifiez si les fichiers ont été téléchargés
        if photo and pdf:
            # Assurez-vous que les noms de fichiers sont sécurisés pour éviter les problèmes de sécurité
            photo_filename = secure_filename(photo.filename)
            pdf_filename = secure_filename(pdf.filename)

            # Définissez le chemin où vous souhaitez stocker les fichiers
            photo_path = os.path.join('media/images/evenement/', photo_filename)
            pdf_path = os.path.join('media/pdfs/evenement/', pdf_filename)

            # Enregistrez les fichiers téléchargés
            photo.save(photo_path)
            pdf.save(pdf_path)

            # Maintenant, vous pouvez créer l'objet Article avec les chemins des fichiers
            nouvel_evenement = Evenement(
                title=title,
                contenu=contenu,
                photo=photo_path,
                pdf=pdf_path,
                date_de_fin= date_de_fin,
                date_de_depart=date_de_depart
            )
            try:
                db.session.add(nouvel_evenement)
                db.session.commit()
                return redirect(url_for('page_admin'))
            except Exception as e:
                db.session.rollback()
                error_message = str(e)  # Convertit l'exception en une chaîne de caractères
                return f"Erreur lors de l'ajout de l'article : {error_message}"

    # Si la méthode est GET ou si le formulaire n'a pas été soumis, affichez simplement le formulaire
    return render_template('Admin/articles.html')


@app.route('/ajout_evenement_form', methods=['GET', 'POST'])
def ajout_evenement_form():
    return render_template('Admin/evenement_form.html')

@app.route('/supprimer_evenement/<int:evenement_id>', methods=['GET', 'POST'])
def supprimer_evenement(evenement_id):
    evenement = Evenement.query.get(evenement_id)

    if evenement:
        if request.method == 'GET':
            try:
                # Supprimez l'objet Evenement de la base de données
                db.session.delete(evenement)
                db.session.commit()
                flash('L\'événement a été supprimé avec succès.', 'success')
                return redirect(url_for('page_admin'))
            except Exception as e:
                db.session.rollback()
                error_message = str(e)
                return f"Erreur lors de la suppression de l'événement : {error_message}"

    flash('L\'événement n\'existe pas.', 'danger')
    return redirect(url_for('page_admin'))

@app.route('/editer_evenement/<int:evenement_id>', methods=['GET', 'POST'])
def editer_evenement(evenement_id):
    evenement = Evenement.query.get(evenement_id)

    if evenement:
        if request.method == 'POST':
            # Récupérez les données modifiées du formulaire
            new_title = request.form.get('new_title')
            new_contenu = request.form.get('new_contenu')
            new_date_de_depart_str = request.form.get('new_date_de_depart')
            new_date_de_fin_str = request.form.get('new_date_de_fin')
            new_date_de_fin = datetime.strptime(new_date_de_fin_str, '%Y-%m-%d').date()
            new_date_de_depart = datetime.strptime(new_date_de_depart_str, '%Y-%m-%d').date()

            # Mettez à jour les informations de l'événement
            evenement.title = new_title
            evenement.contenu = new_contenu
            evenement.date_de_depart = new_date_de_depart
            evenement.date_de_fin = new_date_de_fin

            try:
                db.session.commit()
                flash('L\'événement a été modifié avec succès.', 'success')
                return redirect(url_for('page_admin'))
            except Exception as e:
                db.session.rollback()
                error_message = str(e)
                return f"Erreur lors de la modification de l'événement : {error_message}"

        return render_template('Admin/edit_evenement.html', evenement=evenement)

    flash('L\'événement n\'existe pas.', 'danger')
    return redirect(url_for('page_admin'))



### educations
@app.route('/educations')
def educations():
    educations = Education.query.all()
    return render_template('Admin/educations.html', educations=educations)


@app.route('/ajouter_education', methods=['POST'])
def ajouter_education():
    if request.method == 'POST':
        programme = request.form['programme']
        nom = request.form['nom']
        description = request.form['description']
        photo = request.files['photo']  # Accédez au fichier photo
        pdf = request.files['pdf']  # Accédez au fichier PDF
        duree = request.form['duree']
        date_debut_str = request.form['date_de_depart']
        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()

        # Vérifiez si les fichiers ont été téléchargés
        if photo and pdf:
            # Assurez-vous que les noms de fichiers sont sécurisés pour éviter les problèmes de sécurité
            photo_filename = secure_filename(photo.filename)
            pdf_filename = secure_filename(pdf.filename)

            # Définissez le chemin où vous souhaitez stocker les fichiers
            photo_path = os.path.join('media/images/education/', photo_filename)
            pdf_path = os.path.join('media/pdfs/education/', pdf_filename)

            # Enregistrez les fichiers téléchargés
            photo.save(photo_path)
            pdf.save(pdf_path)

            # Maintenant, vous pouvez créer l'objet Article avec les chemins des fichiers
            nouvel_education = Education(

                programme = programme,
                nom = nom,
                description = description,
                photo=photo_path,
                pdf=pdf_path,
                duree = duree,
                date_debut = date_debut
            )
            try:
                db.session.add(nouvel_education)
                db.session.commit()
                return redirect(url_for('page_admin'))
            except Exception as e:
                db.session.rollback()
                error_message = str(e)  # Convertit l'exception en une chaîne de caractères
                return f"Erreur lors de l'ajout de l'article : {error_message}"

    # Si la méthode est GET ou si le formulaire n'a pas été soumis, affichez simplement le formulaire
    return render_template('Admin/articles.html')

@app.route('/ajout_education_form', methods=['GET', 'POST'])
def ajout_education_form():
    return render_template('Admin/education_form.html')

@app.route('/editer_education/<int:education_id>', methods=['GET', 'POST'])
def editer_education(education_id):
    education = Education.query.get(education_id)

    if education:
        if request.method == 'POST':
            # Récupérez les données modifiées du formulaire
            new_programme = request.form.get('new_programme')
            new_nom = request.form.get('new_nom')
            new_description = request.form.get('new_description')
            new_duree = request.form.get('new_duree')
            new_date_debut_str = request.form.get('new_date_debut')
            new_date_debut = datetime.strptime(new_date_debut_str, '%Y-%m-%d').date()

            # Mettez à jour les informations de l'éducation
            education.programme = new_programme
            education.nom = new_nom
            education.description = new_description
            education.duree = new_duree
            education.date_debut = new_date_debut

            try:
                db.session.commit()
                flash('L\'éducation a été modifiée avec succès.', 'success')
                return redirect(url_for('page_admin'))
            except Exception as e:
                db.session.rollback()
                error_message = str(e)
                return f"Erreur lors de la modification de l'éducation : {error_message}"

        return render_template('Admin/edit_education.html', education=education)

    flash('L\'éducation n\'existe pas.', 'danger')
    return redirect(url_for('page_admin'))

@app.route('/supprimer_education/<int:education_id>', methods=['GET', 'POST'])
def supprimer_education(education_id):
    education = Education.query.get(education_id)

    if education:
        if request.method == 'GET':
            try:
                # Supprimez l'objet Éducation de la base de données
                db.session.delete(education)
                db.session.commit()
                flash('L\'éducation a été supprimée avec succès.', 'success')
                return redirect(url_for('page_admin'))
            except Exception as e:
                db.session.rollback()
                error_message = str(e)
                return f"Erreur lors de la suppression de l'éducation : {error_message}"

    flash('L\'éducation n\'existe pas.', 'danger')
    return redirect(url_for('page_admin'))
















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






if __name__ == '__main__':
    with app.app_context():
        db.create_all()    
    app.run(debug=True)
