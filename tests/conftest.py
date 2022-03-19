from datetime import datetime
from random import random

import pytest
from app import create_app
from app.models import Cache, City, Temperature, TemperatureList


@pytest.fixture(scope="function")
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def cities():
    return [City(name=c, address=c, lat=random(), lon=random()) for c in "ABCBDEFGHI"]


@pytest.fixture(scope="function")
def temperatures(cities):
    return [
        Temperature(
            temp_avg=random(),
            temp_max=random(),
            temp_min=random(),
            req_time=datetime.now(),
            city=city,
        )
        for city in cities
    ]


@pytest.fixture(scope="function")
def temperature_list(temperatures):
    return TemperatureList(data=temperatures)


@pytest.fixture(scope="function")
def cache_full(temperatures):
    return Cache(items={t.city.name: t for t in temperatures}, cache_ttl=3600)
