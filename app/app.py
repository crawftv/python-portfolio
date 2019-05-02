from flask import Flask, render_template
from app.firestore import get_medium, db, get_github_events, get_projects

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
        labels, data = get_github_events(db)
        return render_template("github.html",labels=labels, data=data)

    @app.route('/projects')
    def projects():
        projects = get_projects(db)
        return render_template('projects.html', projects = projects)
    
    @app.route('/twitter')
    def twitter():
        return render_template('twitter.html')






    return app
