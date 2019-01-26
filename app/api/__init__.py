from flask import Flask
from flask_restplus import Api
import logging
from werkzeug.contrib.fixers import ProxyFix

client = None
api = Api()
app = Flask(__name__, template_folder='templates', static_folder='static')


def create_app():

    logging.info('create_app')
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    from .endpoints import main_blueprint
    app.register_blueprint(main_blueprint)
    api.init_app(app)

    return app
