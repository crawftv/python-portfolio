from flask import Flask, render_template
from firestore import get_medium, db, get_github_events, get_projects


application = Flask(__name__)


@application.route('/')
def root():
    return render_template('root.html')

@application.route('/blog')
def blog():
    blog_list = get_medium(db)
    return render_template("blog.html",blog_list = blog_list)

@application.route('/github')
def github():
    labels, data = get_github_events(db)
    return render_template("github.html",labels=labels, data=data)

@application.route('/projects')
def projects():
    projects = get_projects(db)
    return render_template('projects.html', projects = projects)

@application.route('/twitter')
def twitter():
    return render_template('twitter.html')

if __name__ == "__main__":
    application.run()
