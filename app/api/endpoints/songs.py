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

print(config.index_path)
#util = ContentUtil(config.songs_data_path, config.index_path)
dataset = DatasetApi()

@ns.route('/<query>')
class Songs(Resource):
    @api.doc('query')
    def get(self, query):
        logger.info(f"Calling get for SONGS with query = {query}")
        try:
            ids = util.get_songs(query, 10)
            mapping = {str(i[0]):i[1] for i in list(zip(ids[0][0],ids[1][0]))}
            ids_list = ' '.join(str(id) for id in ids[0][0])
            logger.info(f"Retireved data: {ids_list}")
            songs = dataset.get_songs_by_id(ids[0][0])
            return sorted([{
                'id': song['id'],
                'name': song['name'],
                'artist': song['artist'],
                'score': f"{mapping[str(song['id'])]:1.10f}"

            } for song in songs],key=lambda x: x['score'], reverse= True)
        except Exception as ex:
            logger.error(str(ex))
            abort(500,str(ex))

