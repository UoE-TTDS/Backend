import api
from flask import Blueprint
from flask_restplus import Resource
from dataset import DatasetApi as DA
from utils import Configuration
from embeddings import ContentUtil

api = api.api
ns = api.namespace('topics/similar/', description='Endpoint for Topics')

logger = Configuration.get_logger()

util = ContentUtil()

@ns.route('/<query>')
class Topics(Resource):
    @api.doc('query')
    def get(self, query):
        logger.info(f"Calling get for SONGS with query = {query}")
        logger.info(f"Calling ContentUtil = {query}")
        data = util.get_songs(query,10)
        try:
            return [data]
        except Exception as ex:
            logger.error(str(ex))
