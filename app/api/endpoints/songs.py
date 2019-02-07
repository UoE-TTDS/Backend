import api
from flask import Blueprint
from flask_restplus import Resource
from dataset import DatasetApi
from utils import Configuration
from flask import abort
from embeddings import ContentUtil

api = api.api
ns = api.namespace('songs', description='Endpoint for songs')

simple_page = Blueprint('songs', __name__)

logger = Configuration.get_logger()
config = Configuration.get_config()

util = ContentUtil(config.songs_data_path, config.index_path)
dataset = DatasetApi()

@ns.route('/<query>')
class Songs(Resource):
    @api.doc('query')
    def get(self, query):
        logger.info(f"Calling get for SONGS with query = {query}")
        try:
            ids = util.get_songs(query, 10)
            ids_list = ' '.join([str(id) for id in ids])
            logger.info(f"Retireved {ids_list}")
            songs = dataset.get_songs_by_id(ids)
            return [{
                'id': song['id'],
                'name': song['title'],
                'artist': song['artist']

            } for song in songs]
        except Exception as ex:
            logger.error(str(ex))
            abort(500,str(ex))

