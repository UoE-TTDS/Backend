from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app, version='0.1', title='TTDS API')


@app.route('/test')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
