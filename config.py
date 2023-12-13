from os import environ


class Config(object):
    """
    Configuración base.
    """
    TG_TOKEN_KEY = environ.get("TG_TOKEN_KEY")
    CHAT_ID = environ.get("TG_CHAT_ID")
    PORT = environ.get("PORT")
    DEBUG = environ.get("DEBUG")
    DB_USER = environ.get("DB_USER")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    DB_PORT = environ.get("DB_PORT")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
