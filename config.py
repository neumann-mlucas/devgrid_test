import os


class Config(object):
    API_KEY = os.environ.get("API_KEY", "")
    CACHE_TTL = os.environ.get("CACHE_TTL", 3600)
    DEBUG = os.environ.get("DEBUG", True)
    DEFAULT_MAX_NUMBER = os.environ.get("DEFAULT_MAX_NUMBER", 10)
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret")
