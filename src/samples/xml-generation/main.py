from csv_to_xml_converter import CSVtoXMLConverter

if __name__ == "__main__":
    converter = CSVtoXMLConverter(r"../../../docker/volumes/data/dataset.csv")
    print(converter.to_xml_str())

    output_xml_path = r"../../../docker/volumes/data/output.xml"

    xml_str = converter.to_xml_str()

    # Save the XML string to a file
    with open(output_xml_path, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_str)
