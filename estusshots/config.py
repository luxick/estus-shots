from configparser import ConfigParser


class Config:
    def __init__(self):
        parser = ConfigParser()
        parser.read("config.ini")
        self.SECRET_KEY = parser.get("Default", "ES_SECRET_KEY")
        self.WRITE_PW = parser.get("Default", "ES_WRITE_PW")
        self.READ_PW = parser.get("Default", "ES_READ_PW")
        self.DATABASE_PATH = parser.get("Default", "ES_DATABASE_PATH")
        self.LOG_PATH = parser.get("Default", "ES_LOG_PATH")


config = Config()

