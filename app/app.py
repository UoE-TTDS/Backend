import os
from api import create_app
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)
logging.info("This works")

if __name__ == "__main__":
    app = create_app()
    app.run(host='localhost')
