from flask import Flask
from flask_restplus import Api
from werkzeug.contrib.fixers import ProxyFix
client = None
api = Api()

def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    from .endpoints import main_blueprint
    app.register_blueprint(main_blueprint)
    api.init_app(app)
    return app
