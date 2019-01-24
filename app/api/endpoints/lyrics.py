import api
from flask import Blueprint
from flask_restplus import Resource

api = api.api
ns = api.namespace('lyrics', description='Endpoint for lyrics ')

simple_page = Blueprint('lyrics', __name__)

@ns.route('/<query>')
class Lyrics(Resource):
    @api.doc('query')
    def get(self, query):
        return {query: 'THOSE ARE SOME LYRICS'}
    