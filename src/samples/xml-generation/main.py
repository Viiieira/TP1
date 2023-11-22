from csv_to_xml_converter import CSVtoXMLConverter

if __name__ == "__main__":
    converter = CSVtoXMLConverter(r"C:\Users\vitor\OneDrive\Ambiente de Trabalho\E.I\IS\TP1\docker\volumes\data\winemag-data_first150k.csv")
    print(converter.to_xml_str())
