import api
from flask import Blueprint
from flask_restplus import Resource
from dataset import DatasetApi as DA
from utils import Configuration

api = api.api
ns = api.namespace('song', description='Endpoint for songs')

simple_page = Blueprint('song', __name__)

logger = Configuration.get_logger()


@ns.route('/<id>')
class Song(Resource):
    @api.doc('id')
    def get(self, id):
        logger.info(f"Calling get for SONG with id = {id}")
        try:
            song = DA.get_song_by_id(id)
            return song
        except Exception as ex:
            logger.error(str(ex))
