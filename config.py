from os import environ


class Config(object):
    """
    Configuración base.
    """
    JSON_SORT_KEYS = False
    BASIC_AUTH_USERNAME = environ.get('AUTH_USERNAME')
    BASIC_AUTH_PASSWORD = environ.get('AUTH_PASSWORD')
    TG_TOKEN_KEY = environ.get("TG_TOKEN_KEY")
    CHAT_ID = environ.get("TG_CHAT_ID")
    APP_RUN_HOST = environ.get("APP_RUN_HOST", "0.0.0.0")
    PORT = environ.get("PORT", 5000)
    DEBUG = environ.get("DEBUG", False)
    DB_USER = environ.get("DB_USER", "falconfeeds")
    DB_PASSWORD = environ.get("DB_PASSWORD", "falconfeeds")
    DB_HOST = environ.get("DB_HOST", "host.docker.internal")
    DB_NAME = environ.get("DB_NAME", "falconfeeds")
    DB_PORT = environ.get("DB_PORT", 3306)
    DB_TYPE = environ.get("DB_TYPE", "mysql+mysqlconnector")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
