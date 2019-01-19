import api
import os

version = os.getenv('versionnumber', 'default')

if __name__ == "__main__":
    app = api.create_app()
    app.run(host='0.0.0.0')
