import psycopg2

connection = None
cursor = None

try:
    connection = psycopg2.connect(user="postgres", password="123", host="is-db", port="5432", database="is")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM imported_documents")

    print("XML Documents list:")
    for document in cursor:
        print(f" > {document[0]}, from {document[1]}")


except (Exception, psycopg2.Error) as error:
    print("Failed to fetch data", error)

finally:
    if connection:
        cursor.close()
        connection.close()