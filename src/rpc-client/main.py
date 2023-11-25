import xmlrpc.client

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

string = "hello world"



print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")

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
    print("\t0 -Exit")

    choice = input("Enter your choice: ")

    if(choice == '1'):
        input_id = input("Import a XML File to the Database: ")
        print(input_id)
        query = "UPDATE public.imported_documents SET deleted = TRUE WHERE id = {input_id};"
        print(f" > {server.execute_query(query)}")
    elif(choice == '2'):
        query = "SELECT * FROM public.imported_documents;"
        results = server.execute_query(query)

    elif(choice == '3'):
        input_id = input("Enter the ID to be deleted: ")
        print(input_id)
        query = "UPDATE public.imported_documents SET deleted = TRUE WHERE id = {input_id};"
        print(f" > {server.execute_query(query)}")

    elif(choice == '4'):
        query = "SELECT DISTINCT xpath('/WineReviews/Countries/Country/@name', xml)::text AS country_name FROM public.imported_documents;"
        print(f" > {server.execute_query(query)}")

    elif(choice == '5'):
        country_name = input("Enter the country name (e.g.,Portugal):")
        query = "SELECT xpath('/WineReviews/Countries/Country[@name=\"{country_name}\"]/Wines/Wine/@name', xml)::text AS wine_name FROM public.imported_documents;"
        print(f" > {server.execute_query(query)}")

    elif(choice == '6'):
        operator = input("Enter the operator (e.g., >, <, >=, <=, =): ")
        points = input("Enter the points: ")
    
        # Construct the XPath query based on input
        query = f"SELECT xpath('/WineReviews/Countries/Country[Wines/Wine[@points {operator} {points}]]/Wines/Wine/@name', xml)::text AS wine_name, " \
                f"xpath('/WineReviews/Countries/Country[Wines/Wine[@points {operator} {points}]]/Wines/Wine/@price', xml)::text AS wine_price " \
                f"FROM public.imported_documents;"  
        print(f"query: {query}")
        print(f" > {server.execute_query(query)}")
    
    elif choice == '7':
        country_name = input("Enter the country name (e.g., Portugal): ")
        
        # Choose the field for grouping (e.g., points)
        group_field = input("Enter the field for grouping (e.g., points): ")
        
        # Construct the XPath query based on input
        query = f"SELECT xpath('/WineReviews/Countries/Country[@name=\"{country_name}\"]/Wines/Wine/@{group_field}', xml)::text AS group_field, " \
                f"xpath('/WineReviews/Countries/Country[@name=\"{country_name}\"]/Wines/Wine/@name', xml)::text AS wine_name " \
                f"FROM public.imported_documents GROUP BY group_field;"


    if(choice == '0'):
        print("Exiting...")
        break