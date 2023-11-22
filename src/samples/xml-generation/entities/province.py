import xml.etree.ElementTree as ET


class Province:

    def __init__(self, name):
        Province.counter += 1
        self._id = Province.counter
        self._name = name

    def to_xml(self):
        el = ET.Element("Wine")
        el.set("id", str(self._id))
        el.set("name", self._name)
        return el
    
    def get_id(self):
        return self._id

    def __str__(self):
        return f"{self._name}"


Province.counter = 0
