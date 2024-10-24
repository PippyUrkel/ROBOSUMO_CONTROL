from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b24dae022b0bcb79e3a7d3bd1971670a'

    from .views import views
    # from .auth import auth

    app.register_blueprint(views, url_prefix='/')
  
    return app