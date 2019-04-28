from flask import Flask


def create_app():
    app = Flask(__name__)


    @app.route('/')
    def root():
        return render_template('root.html')

    @app.route('/blog')
    def topic():
        return render_template("blog.html")

    









    return app
