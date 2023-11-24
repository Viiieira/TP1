import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from csv_reader import CSVReader
from entities.country import Country
from entities.wine import Wine
from entities.province import Province


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):

        # read countries
        countries = self._reader.read_entities(
            attr="country",
            builder=lambda row: Country(row["country"])
        )

         # read countries
        provinces = self._reader.read_entities(
            attr="province",
            builder=lambda row: Province(row["province"])
        )

        # read players

        def after_creating_wine(wine, row):
            # add the wine to the appropriate province
            countries[row["country"]].add_wine(wine)

        self._reader.read_entities(
            attr="designation",
            builder=lambda row: Wine(
                name=row["designation"],
                points=row["points"],
                price=row["price"],
                province=row["province"]
            ),
            after_create=after_creating_wine
        )

        # generate the final xml
        root_el = ET.Element("WineReviews")

        countries_el = ET.Element("Countries")
        for country in countries.values():
            countries_el.append(country.to_xml())


        root_el.append(countries_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

