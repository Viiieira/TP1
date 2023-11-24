from csv_to_xml_converter import CSVtoXMLConverter
import psycopg2

def insert_xml(xml_filename, xml_str):
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(user="is", password="is", host="is-db", port="5432", database="is")
        cursor = connection.cursor()
        sql = "INSERT INTO imported_documents (file_name, xml) VALUES (%s, %s)"
        cursor.execute(sql, (xml_filename, xml_str))
        connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    converter = CSVtoXMLConverter(r"/data/dataset.csv")
    # print(converter.to_xml_str())

    output_xml_path = r"/data/output.xml"

    xml_str = converter.to_xml_str()

    # Save the XML string to a file
    with open(output_xml_path, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_str)

    # Insert XML to DB
    insert_xml("output.xml", xml_str)