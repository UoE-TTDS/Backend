import api
from flask import Blueprint, abort
from flask_restplus import Resource
from dataset import DatasetApi as DA
from utils import Configuration
from dataset import DatasetApi
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
            if song is None:
                return f'Song with id {id} not found', 404
            DA.log_song(id)
            return song
        except Exception as ex:
            logger.error(str(ex))
            return f'There was an error in processing the request : {str(ex)}', 500
