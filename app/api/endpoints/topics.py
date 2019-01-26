import api
from flask import Blueprint
from flask_restplus import Resource
from dataset import DatasetApi as DA
from utils import Configuration

api = api.api
ns = api.namespace('topics/similar/', description='Endpoint for Topics')

logger = Configuration.get_logger()


@ns.route('/<query>')
class Topics(Resource):
    @api.doc('query')
    def get(self, query):
        logger.info(f"Calling get for SONGS with query = {query}")
        try:
            return [f"topic-similar-to-{query}-number{i}" for i in range(5)]
        except Exception as ex:
            logger.error(str(ex))
