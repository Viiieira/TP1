import psycopg2
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import xml.dom.minidom as md


class Wine:

    def __init__(self, name, points, price, province, variety):
        Wine.counter += 1
        self._id = Wine.counter
        self._name = name
        self._points = points
        self._price = price
        self._province = province
        self._variety = variety

    def to_xml(self):
        el = ET.Element("Wine")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("points", self._points)
        el.set("price", self._price)
        el.set("variety", self._variety)
        el.set("province", self._province)
        return el

    def __str__(self):
        return f"{self._name}, points:{self._points}, price:{self._price}, variety:{self._variety}, province:{self._province}"

Wine.counter = 0
