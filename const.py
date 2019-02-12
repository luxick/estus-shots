import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

DATABASE_NAME = "es_debug.db"
DATABASE_PATH = os.path.join(BASE_PATH, DATABASE_NAME)

LOG_NAME = "estus-shots.log"
LOG_PATH = os.path.join(BASE_PATH, LOG_NAME)
