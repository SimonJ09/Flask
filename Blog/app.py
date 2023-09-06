from flask import Flask, render_template
from db import Post
app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True, port=3000)
