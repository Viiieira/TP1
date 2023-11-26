import xmlrpc.client

print("Connecting to server...")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

while True:
    print("\nSelect one of the following options:")
    print("\nFile Management:")
    print("\t1 - Import a XML file to the Database")
    print("\t2 - List XML Files in the Database")
    print("\t3 - Delete a XML File from the Database")
    print("\nData Views:")
    print("\t4 - List All Countries")
    print("\t5 - List All Wines of a Country")
    print("\t6 - List Average Points of Wines of a Province")
    print("\t7 - List Average Points of Wines of a Province")
    print("\t0 - Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        try:
            input_id = int(input("Import a XML File to the Database: "))
            print(input_id)

            query = f"UPDATE public.imported_documents SET deleted = TRUE WHERE id = %s;"
            print(f" > {server.execute_query(query, (input_id,))}")
        except Exception as e:
            print(f"> Error executing query: {e}")
    elif choice == 2:
        try:
            # Select all XML files that are not soft-deleted
            query = "SELECT file_name, created_on, updated_on, deleted FROM public.imported_documents;"
            results = server.execute_query(query)

            if results:
                # Assuming all values are in the first (and only) row
                row = results[0]

                for column, value in zip(["File", "Created On", "Updated On", "Deleted"], row):
                    if column in ["Created On", "Updated On"]:
                        # Convert the value to string and format
                        formatted_value = str(value).replace("T", " ").replace("-", "/")
                        # Switch the position of the day and the month
                        formatted_value = (formatted_value[6:8] + "/" + formatted_value[4:6] + "/" + formatted_value[0:4]
                                           + f" {formatted_value[9:]}")
                    else:
                        formatted_value = str(value)

                    print(f"{column}: {formatted_value}")

            else:
                print("No results found.")

        except Exception as e:
            print(f"Error executing query: {e}")

    elif choice == 3:
        try:
            select_query = "SELECT id, file_name FROM public.imported_documents WHERE deleted = FALSE"
            results = server.execute_query(select_query)
            if len(results) > 0:
                print(f"> ID: {results[0][0]}, File: {results[0][1]}")

                input_id = input("Enter the ID to be soft-deleted: ")
                print(f"Introduced ID by the user: {input_id}")

                # Check if the record is already soft-deleted
                check_query = "SELECT deleted FROM public.imported_documents WHERE id = %s;"
                current_deleted_status = server.execute_query(check_query, (input_id,))

                if current_deleted_status and current_deleted_status[0][0]:
                    print("Warning: This record is already soft-deleted.")
                else:
                    update_query = "UPDATE public.imported_documents SET deleted = TRUE WHERE id = %s;"
                    print(f" > {server.execute_query(update_query, (input_id,))}")
                    print(f"Record {input_id} has been successfully soft-deleted.")
            else:
                print("There is no files to be deleted.")

        except Exception as e:
            print(f"Error executing query: {e}")

    elif choice == 4:
        query = "SELECT DISTINCT xpath('/WineReviews/Countries/Country/@name', xml)::text AS country_name FROM public.imported_documents;"
        print(f" > {server.execute_query(query)}")

    elif choice == 5:
        country_name = input("Enter the country name (e.g.,Portugal):")
        query = "SELECT xpath('/WineReviews/Countries/Country[@name=\"{country_name}\"]/Wines/Wine/@name', xml)::text AS wine_name FROM public.imported_documents;"
        print(f" > {server.execute_query(query)}")

    elif choice == 6:
        operator = input("Enter the operator (e.g., >, <, >=, <=, =): ")
        points = input("Enter the points: ")
    
        # Construct the XPath query based on input
        query = f"SELECT xpath('/WineReviews/Countries/Country[Wines/Wine[@points {operator} {points}]]/Wines/Wine/@name', xml)::text AS wine_name, " \
                f"xpath('/WineReviews/Countries/Country[Wines/Wine[@points {operator} {points}]]/Wines/Wine/@price', xml)::text AS wine_price " \
                f"FROM public.imported_documents;"  
        print(f"query: {query}")
        print(f" > {server.execute_query(query)}")
    
    elif choice == 7:
        country_name = input("Enter the country name (e.g., Portugal): ")
        
        # Choose the field for grouping (e.g., points)
        group_field = input("Enter the field for grouping (e.g., points): ")
        
        # Construct the XPath query based on input
        query = f"SELECT xpath('/WineReviews/Countries/Country[@name=\"{country_name}\"]/Wines/Wine/@{group_field}', xml)::text AS group_field, " \
                f"xpath('/WineReviews/Countries/Country[@name=\"{country_name}\"]/Wines/Wine/@name', xml)::text AS wine_name " \
                f"FROM public.imported_documents GROUP BY group_field;"

    elif choice == 0:
        print("Exiting...")
        break