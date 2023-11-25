import psycopg2

def execute_query(query):
    connection = None
    cursor = None
    result = []

    try:
        connection = psycopg2.connect(user="postgres", password="123", host="is-db", port="5432", database="is")
        cursor = connection.cursor()

        cursor.execute(query)
        connection.commit()

        result = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error executing the query:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return result

query = "SELECT * FROM imported_documents"
results = execute_query(query)

for row in results:
    print(row)
