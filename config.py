import json
import os


def roles():
    with open("roles.json", "r") as f:
        return json.load(f)


class Config:
    SECRET_KEY = os.environ.get("ES_SECRET_KEY")
