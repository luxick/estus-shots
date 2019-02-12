import os


class Config:
    SECRET_KEY = os.environ.get("ES_SECRET_KEY")
    WRITE_PW = os.environ.get("ES_WRITE_PW")
    READ_PW = os.environ.get("ES_READ_PW")
