import os
import logging
import sys

from flask import Flask
from flask_bootstrap import Bootstrap


from estusshots.config import config


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


if not config.SECRET_KEY:
    logging.error(
        "No secret key provided for app. Are the environment variables set correctly?"
    )
    sys.exit(1)

app = create_app()

logging.basicConfig(filename=config.LOG_PATH, level=logging.DEBUG)
logging.info(f"Starting in working dir: {os.getcwd()}")
app.config.from_object(config)

import estusshots.views.drinks
import estusshots.views.enemies
import estusshots.views.episodes
import estusshots.views.events
import estusshots.views.login
import estusshots.views.players
import estusshots.views.seasons
