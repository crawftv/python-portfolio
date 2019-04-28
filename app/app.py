from flask import Flask, render_template
from app.firestore import get_medium, db

def create_app():
    app = Flask(__name__)


    @app.route('/')
    def root():
        return render_template('root.html')

    @app.route('/blog')
    def blog():
        blog_list = get_medium(db)
        return render_template("blog.html",blog_list = blog_list)

    @app.route('/github')
    def github():

        return render_template("github.html")









    return app
