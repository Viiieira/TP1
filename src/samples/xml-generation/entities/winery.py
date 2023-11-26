import xml.etree.ElementTree as ET

class Winery:

    def __init__(self, winery, province):
        Winery.counter += 1
        self._id = Winery.counter
        self._winery = winery
        self._province = province

    def to_xml(self):
        el = ET.Element("Winery")
        el.set("id", str(self._id))
        el.set("winery", self._winery)
        el.set("province", self._province)

        return el
    
    def get_id(self):
        return self._id

    def __str__(self):
        return f" ({self._id}, {self._winery}, {self._province})"

Winery.counter = 0
