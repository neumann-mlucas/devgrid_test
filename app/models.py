from datetime import datetime

from pydantic import BaseModel
from toolz import valfilter


class City(BaseModel):
    request_name: str = ""
    name: str = ""
    address: str = ""
    country: str = ""
    lat: float = float("nan")
    lon: float = float("nan")


class Temperature(BaseModel):
    temp_avg: float = float("nan")
    temp_max: float = float("nan")
    temp_min: float = float("nan")
    feels_like: float = float("nan")
    req_time: datetime = datetime.utcnow()
    city: City


class TemperatureList(BaseModel):
    data: list[Temperature]


class Cache(BaseModel):
    items: dict[str, Temperature] = {}
    cache_ttl: int

    def clean(self) -> None:
        get_dt = lambda dt: (datetime.utcnow() - dt).total_seconds()
        self.items = {
            city: temp
            for (city, temp) in self.items.items()
            if get_dt(temp.req_time) <= self.cache_ttl
        }

    def add(self, city: str, temperature: Temperature) -> None:
        self.clean()
        self.items[city] = temperature
