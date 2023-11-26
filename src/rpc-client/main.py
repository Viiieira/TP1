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
    print("\t4 - List All Wines belonging to a country")
    print("\t5 - List All Wines that match an input amount of points")
    print("\t6 - List Wineries grouped by Province")
    print("\t7 - List Wineries ordered by Name ")
    print("\t8 - List Average Points of Wines of a Province")
    print("\t0 - Exit")

    choice = int(input("Enter your choice: "))

    match choice:
        case 1:
            try:
                input_id = int(input("Import a XML File to the Database: "))
                print(input_id)

                query = f"UPDATE public.imported_documents SET deleted = TRUE WHERE id = %s;"
                print(f" > {server.execute_query(query, (input_id,))}")
            except Exception as e:
                print(f"> Error executing query: {e}")

        case 2:
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
                            formatted_value = (
                                        formatted_value[6:8] + "/" + formatted_value[4:6] + "/" + formatted_value[0:4]
                                        + f" {formatted_value[9:]}")
                        else:
                            formatted_value = str(value)

                        print(f"{column}: {formatted_value}")

                else:
                    print("No results found.")

            except Exception as e:
                print(f"Error executing query: {e}")

        case 3:
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

        case 4:
            try:
                country = input("Enter a country (e.g., Spain): ")

                query = f"SELECT xpath('/WineReviews/Countries/Country[@name=\"{country}\"]/Wines/Wine/@name', xml) AS wine_names FROM public.imported_documents;"

                results = server.execute_query(query)

                if len(results) > 0:
                    # Extracting the wine names from the result
                    wines_str = results[0][0]

                    # Handling the case when there are multiple wine names
                    if wines_str:
                        wines_list = wines_str.split(',')

                        # Iterating over the list and printing each wine name
                        for wine in wines_list:
                            print(f"> {wine.strip()}")
                    else:
                        print(f"There are no wines for the country: {country}")
                else:
                    print(f"There are no wines for the country: {country}")

            except Exception as e:
                print(f"Error executing query: {e}")

        case 5:
            operator = input("Enter the operator (e.g., >, <, >=, <=, =): ")
            points = input("Enter the points: ")

            # Construct the XPath query based on input
            query = f"SELECT xpath('/WineReviews/Countries/Country[Wines/Wine[@points {operator} {points}]]/Wines/Wine/@name', xml)::text AS wine_name " \
                    f"FROM public.imported_documents;"

            try:
                results = server.execute_query(query)

                if len(results) > 0:
                    # Extracting the wines names from the result
                    names_str = results[0][0]

                    # Removing curly braces and quotes
                    names_string = names_str.replace('{', '').replace('}', '').replace('"', '')

                    # Splitting the string into a list of countries
                    names_list = names_string.split(',')

                    # Iterating over the list and printing each country
                    for name in names_list:
                        print(f"> {name.strip()}")
                else:
                    print("No wines match the criteria.")

            except Exception as e:
                print(f"Error executing query: {e}")

        case 6:
            try:
                # Construct the XPath query to get all wineries grouped by province
                query = """
                        SELECT 
                            unnest(xpath('/WineReviews/Wineries/Winery/@winery', xml))::text AS winery_name,
                            unnest(xpath('/WineReviews/Wineries/Winery/@province', xml))::text AS province
                        FROM public.imported_documents
                        ORDER BY province, winery_name;
                        """

                results = server.execute_query(query)

                if len(results) > 0:
                    # Extracting and printing the wineries grouped by province
                    current_province = None
                    for winery_data in results:
                        winery_name = winery_data[0].strip('"')
                        province = winery_data[1].strip('"')

                        # Print province header when it changes
                        if province != current_province:
                            print(f"Province: {province}")
                            current_province = province

                        print(f"> Winery Name: {winery_name}")
                else:
                    print("No wineries found.")

            except Exception as e:
                print(f"Error executing query: {e}")


        case 7:
            try:
                # Construct the XPath query to get all wineries ordered by name
                query = """
                        SELECT 
                            unnest(xpath('/WineReviews/Wineries/Winery/@winery', xml))::text AS winery_name
                        FROM public.imported_documents
                        ORDER BY winery_name;
                        """

                results = server.execute_query(query)

                if len(results) > 0:
                    # Extracting and printing the wineries ordered by name
                    for winery_data in results:
                        winery_name = winery_data[0].strip('"')
                        print(f"> Winery Name: {winery_name}")
                else:
                    print("No wineries found.")

            except Exception as e:
                print(f"Error executing query: {e}")

        case 8:
            try:
                country = input("Enter a country (e.g., Italy): ")

                # Construct the XPath query to get wines from the input country and their respective tasters
                query = f"""
                        SELECT 
                            unnest(xpath('/WineReviews/Countries/Country[@name="{country}"]/Wines/Wine/@name', xml))::text AS wine_name,
                            unnest(xpath('/WineReviews/Countries/Country[@name="{country}"]/Wines/Wine/@taster_ref', xml))::text AS taster_ref,
                            xpath('/WineReviews/Tasters/Taster[@id=unnest(xpath('/WineReviews/Countries/Country[@name="{country}"]/Wines/Wine/@taster_ref', xml))::text)]/@taster_name', xml)::text AS taster_name,
                            xpath('/WineReviews/Tasters/Taster[@id=unnest(xpath('/WineReviews/Countries/Country[@name="{country}"]/Wines/Wine/@taster_ref', xml))::text)]/@taster_twitter_handle', xml)::text AS taster_twitter_handle
                        FROM public.imported_documents
                        WHERE xpath('/WineReviews/Countries/Country/@name', xml) = '{country}';
                        """

                results = server.execute_query(query)

                if len(results) > 0:
                    # Extracting and printing the wines and their respective tasters
                    for wine_data in results:
                        wine_name = wine_data[0].strip('"')
                        taster_ref = wine_data[1].strip('"')
                        taster_name = wine_data[2].strip('"')
                        taster_twitter_handle = wine_data[3].strip('"')

                        print(f"> Wine Name: {wine_name}")
                        print(f"  Taster Name: {taster_name}, Taster Twitter Handle: {taster_twitter_handle}")
                else:
                    print(f"No wines found for the country: {country}")

            except Exception as e:
                print(f"Error executing query: {e}")






        case 0:
            print("Exiting...")
            break

        case _:
            print("This is not a valid option. Try again")