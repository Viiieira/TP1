import xmlrpc.client

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

string = "hello world"



print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")

while True:
    print("\nSelect one of the following options:")
    print("\t1 - List All Countries")
    print("\t2 - List All Wines of a Country")
    print("\t3 - List Average Points of Wines of a Province")
    print("\t0 -Exit")

    choice = input("Enter your choice: ")

    if(choice == '1'):
        query = "SELECT DISTINCT xpath('/WineReviews/Countries/Country/@name', xml)::text AS country_name FROM public.imported_documents;"
        print(f" > {server.execute_query(query)}")

    elif(choice == '2'):
        country_name = input("Enter the country name (e.g.,Portugal):")
        query = "SELECT xpath('/WineReviews/Countries/Country[@name=\"{country_name}\"]/Wines/Wine/@name', xml)::text AS wine_name FROM public.imported_documents;"
        print(f" > {server.execute_query(query)}")

    elif(choice == '3'):
        operator = input("Enter the operator (e.g., >, <, >=, <=, =): ")
        points = input("Enter the points: ")
    
        # Construct the XPath query based on input
        query = f"SELECT xpath('/WineReviews/Countries/Country[Wines/Wine[@points {operator} {points}]]/Wines/Wine/@name', xml)::text AS wine_name, " \
                f"xpath('/WineReviews/Countries/Country[Wines/Wine[@points {operator} {points}]]/Wines/Wine/@price', xml)::text AS wine_price " \
                f"FROM public.imported_documents;"  
        print(f"query: {query}")
        print(f" > {server.execute_query(query)}")
    
    elif choice == '4':
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