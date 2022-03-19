from functools import cache

import requests
from app.main import bp
from app.models import City, Temperature, TemperatureList
from flask import current_app, request
from geopy.geocoders import Nominatim
from toolz import tail

URL = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"


@cache
def find_coordinates(city_name: str) -> City:
    """given a city name find its coordinates and returns a City obj"""
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city_name)
    return (
        City(
            request_name=city_name,
            address=location.address,
            lat=location.latitude,
            lon=location.longitude,
        )
        if location
        else City()
    )


def parse_response(resp: dict, city: City) -> Temperature:
    """parse json response from Weather API into a Temperature Obj"""
    data = resp.get("main", {})
    city.country = resp.get("sys", {}).get("country", "")
    city.name = resp.get("name", city.name)
    return Temperature(
        temp_max=data.get("temp_max", float("nan")),
        temp_min=data.get("temp_min", float("nan")),
        temp_avg=data.get("temp", float("nan")),
        feels_like=data.get("temp", float("nan")),
        city=city,
    )


@bp.route("/")
def health():
    return {
        "status": "OK",
        "cache": current_app.cache.json(),
    }


@bp.route("/temperature/<string:city_name>")
def get_city_temperature(city_name: str) -> dict:

    # check if city_name in cache
    if city_name in current_app.cache.items:
        return current_app.cache.items[city_name].json()

    # translate city_name into City obj / coordinates
    city = find_coordinates(city_name)

    # build API url
    url = URL.format(lat=city.lat, lon=city.lon, api_key=current_app.config["API_KEY"])

    resp = requests.get(url)
    # check response and add city to cache
    if resp.ok:
        temp = parse_response(resp.json(), city)
        current_app.cache.items[temp.city.request_name] = temp
        return temp.json()
    else:
        return {"error": "bad request"}, 400


@bp.route("/temperature")
def list_temperature() -> dict:
    # get max_number from argument and validate type
    max_number = request.args.get(
        "max_number", current_app.config["DEFAULT_MAX_NUMBER"]
    )
    try:
        max_number = int(max_number)
    except ValueError:
        return {"error": "bad url argument"}, 400

    # exclude old entries begore returning json
    current_app.cache.clean()
    # get only entries up to max_number
    items = list(tail(max_number, current_app.cache.items.values()))

    return TemperatureList(data=items).json()
