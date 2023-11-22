import xml.etree.ElementTree as ET

from entities.wine import Wine


class Country:

    def __init__(self, name: str):
        Country.counter += 1
        self._id = Country.counter
        self._name = name
        self._wines = []

    def add_wine(self, wine: Wine):
        self._wines.append(wine)

    def to_xml(self):
        el = ET.Element("Country")
        el.set("id", str(self._id))
        el.set("name", self._name)

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
