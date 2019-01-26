import api
from flask import Blueprint
from flask_restplus import Resource
from dataset import DatasetApi as DA
from utils import Configuration

api = api.api
ns = api.namespace('songs', description='Endpoint for songs')

simple_page = Blueprint('songs', __name__)

logger = Configuration.get_logger()


@ns.route('/<query>')
class Songs(Resource):
    @api.doc('query')
    def get(self, query):
        logger.info(f"Calling get for SONGS with query = {query}")
        try:
            return {
                'id': 0,
                'name': 'song title',
                'artist': 'artist name'

            }
        except Exception as ex:
            logger.error(str(ex))
