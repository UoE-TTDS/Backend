"""
The flask application package. This is where we initialize Flask
"""
from flask import Flask
app = Flask(__name__)
wsgi_app = app.wsgi_app #Registering with IIS
import FlaskWeb.views