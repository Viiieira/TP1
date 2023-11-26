import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from entities.wine import Wine


class Country:

    def __init__(self, name: str):
        Country.counter += 1
        self._id = Country.counter
        self._name = name
        self._wines = []
        self._latitude = None
        self._longitude = None
        self.fetch_coordinates()

    def fetch_coordinates(self):
        # Use Nominatim API to fetch coordinates for the country
        endpoint = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": self._name,
            "format": "json",
            "limit": 1,
        }
        url = f"{endpoint}?{urllib.parse.urlencode(params)}"

        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            if data:
                location = data[0]
                self._latitude = float(location.get("lat"))
                self._longitude = float(location.get("lon"))

    def add_wine(self, wine: Wine):
        self._wines.append(wine)

    def to_xml(self):
        el = ET.Element("Country")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("latitude", str(self._latitude))  # Convert to string
        el.set("longitude", str(self._longitude))  # Convert to string

        wines_el = ET.Element("Wines")
        for wine in self._wines:
            wines_el.append(wine.to_xml())

        el.append(wines_el)

        return el
    
    def get_id(self):
        return self._id

    def __str__(self):
        return f"{self._name} ({self._id})"


Country.counter = 0
