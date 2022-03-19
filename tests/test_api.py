import json
from time import sleep

import pytest
import requests
from app.models import Temperature


class TestCitiesTemperature:
    """Test API endpoint '/temperature/<city_name>'"""

    def test_simple_request(self, client):
        response = client.get("temperature/paris")
        json_response = json.loads(response.data)
        assert response.status == "200 OK"
        assert Temperature.parse_obj(json_response)

    def test_add_to_cache(self, app, client):
        response = client.get("temperature/paris")
        assert len(app.cache.items) == 1
        response = client.get("temperature/berlin")
        assert len(app.cache.items) == 2
        response = client.get("temperature/paris")
        assert len(app.cache.items) == 2

    def test_bad_request(self, client):
        response = client.get("temperature/!@#$%")
        json_response = json.loads(response.data)
        assert response.status == "400 BAD REQUEST"
        assert "error" in json_response


class TestListTemperatures:
    """Test API endpoint '/temperature'"""

    def test_empty_cache(self, client):
        response = client.get("temperature")
        json_response = json.loads(response.data)
        assert response.status == "200 OK"
        assert json_response == {"data": []}

    def test_add_to_cache(self, client):
        client.get("temperature/paris")
        client.get("temperature/berlin")
        client.get("temperature/madri")

        response = client.get("temperature")
        json_response = json.loads(response.data)

        assert response.status == "200 OK"
        assert len(json_response.get("data")) == 3

    def test_max_number_argument(self, client):
        client.get("temperature/paris")
        client.get("temperature/berlin")
        client.get("temperature/madri")

        response = client.get("temperature?max_number=2")
        json_response = json.loads(response.data)

        assert response.status == "200 OK"
        assert len(json_response.get("data")) == 2

    def test_bad_argument(self, client):
        response = client.get("temperature?max_number=bad")
        json_response = json.loads(response.data)
        assert response.status == "400 BAD REQUEST"
        assert "error" in json_response

    def test_cache_ttl(self, client, app):
        client.get("temperature/berlin")
        app.cache.cache_ttl = 1
        sleep(2)

        response = client.get("temperature")
        json_response = json.loads(response.data)

        assert response.status == "200 OK"
        assert json_response == {"data": []}
