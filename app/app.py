from api import create_app
import logging
from utils import Configuration

logging.basicConfig(filename='app.log', level=logging.INFO)
logging.info("This works")


app = create_app()

if __name__ == "__main__":
    Configuration.from_file('./config.cfg')
    app.run()
