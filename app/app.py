from flask import Flask
import os
from api import create_app
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)
logging.info("This works")


app = create_app()

if __name__ == "__main__":
    app.run()
