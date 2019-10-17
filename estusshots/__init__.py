import os
import logging

from flask import Flask
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()
app.config.from_pyfile("config/default.py")
config_path = f"config/{app.env}.py"
app.config.from_pyfile(config_path, silent=True)

logging.basicConfig(filename=app.config.get("LOG_PATH"), level=logging.DEBUG)
logging.info(f"Starting in working dir: {os.getcwd()}")

import estusshots.views.drinks
import estusshots.views.enemies
import estusshots.views.episodes
import estusshots.views.events
import estusshots.views.login
import estusshots.views.players
import estusshots.views.seasons
