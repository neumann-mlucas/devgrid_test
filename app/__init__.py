from config import Config
from flask import Flask

from app.models import Cache


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.cache = Cache(cache_ttl=config_class.CACHE_TTL)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
