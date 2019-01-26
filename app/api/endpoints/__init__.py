from flask import Blueprint
main_blueprint = Blueprint('main', __name__)
from .songs import Songs
from .song import Song
from .topics import Topics