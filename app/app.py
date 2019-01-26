from api import create_app
import logging
from utils import Configuration
from flask import render_template
logger = Configuration.get_logger()
app = create_app()


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/search/song')
def song():
    return render_template('song.html')


if __name__ == "__main__":
    logger.info("Application starting")
    app.run()
