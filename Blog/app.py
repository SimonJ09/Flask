
from flask import Flask, render_template
from flask import send_from_directory
from db import Post
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='stactic')

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///C:/Users/AGOHOUNDJE/Documents/Jude/Flask/Blog/database/db.sqlite3'
db = SQLAlchemy(app)
 
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/contact')
def contact():
    return render_template('pages/contact.html')

@app.route('/recherche')
def recherche():
    return render_template('pages/recherche.html')

@app.route('/blog')
def post_index():
    posts=Post.all()
    return render_template('posts/index.html',posts=posts)


@app.route('/service')
def service():
    return render_template('pages/service.html')


@app.route('/education')
def education():
    return render_template('pages/education.html')



def index():
    with app.app_context():
        # You can now safely use the 'db' object within this context
        result = YourModel.query.first()
        return str(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()    
    app.run(debug=True, port=3000)
