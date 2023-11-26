import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from csv_reader import CSVReader
from entities.country import Country
from entities.wine import Wine
from entities.taster import Taster
from entities.winery import Winery

class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):

        # read countries
        countries = self._reader.read_entities(
            attr="country",
            builder=lambda row: Country(row["country"])
        )

        # read tasters
        tasters = self._reader.read_entities(
            attr="taster_name",
            builder=lambda row: Taster(row["taster_name"], row["taster_twitter_handle"])
        )

        # read wineries
        wineries = self._reader.read_entities(
            attr="winery",
            builder=lambda row: Winery(row["winery"], row["province"])
        )

        def after_creating_wine(wine, row):
            # add the wine to the appropriate province
            countries[row["country"]].add_wine(wine)

        self._reader.read_entities(
            attr="designation",
            builder=lambda row: Wine(
                name=row["designation"],
                points=row["points"],
                price=row["price"],
                variety=row["variety"],
                province=row["province"],
                taster=tasters[row["taster_name"]],
                winery=wineries[row["winery"]]
            ),
            after_create=after_creating_wine
        )

        # generate the final xml
        root_el = ET.Element("WineReviews")

        countries_el = ET.Element("Countries")
        for country in countries.values():
            countries_el.append(country.to_xml())

        tasters_el = ET.Element("Tasters")
        for taster in tasters.values():
            tasters_el.append(taster.to_xml())

        wineries_el = ET.Element("Wineries")
        for winery in wineries.values():
            wineries_el.append(winery.to_xml())


        root_el.append(countries_el)
        root_el.append(wineries_el)
        root_el.append(tasters_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

