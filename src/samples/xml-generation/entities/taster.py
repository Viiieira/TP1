import xml.etree.ElementTree as ET

class Taster:

    def __init__(self, name: str, twitter_handle: str):
        Taster.counter += 1
        self._id = Taster.counter
        self._taster_name = name
        self._taster_twitter_handle = twitter_handle

    def to_xml(self):
        el = ET.Element("Taster")
        el.set("id", str(self._id))
        el.set("taster_name", self._taster_name)
        el.set("taster_twitter_handle", self._taster_twitter_handle)

        return el
    
    def get_id(self):
        return self._id

    def __str__(self):
        return f"{self._taster_name} ({self._id})"

Taster.counter = 0
