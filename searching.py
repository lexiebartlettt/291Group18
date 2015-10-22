import cx_Oracle


''' Uses: 
		1. Prompt user for a source, destination and departure date 
		2. For source and destination, the user may enter an airport code
		 or a text that can be used to find an airport code 
		3. If the entered text is not a valid airport code your system s
			should search for airports that have the entered text in their 
			city or name fields (partial match is allowed) and display a 
			list of candidates from which an airport cna be selected by 
			the user. 
		4. Your search for source and destination must be case insensitive 
		5. Your system should search for flights between the source and 
			destination on the given date(s) and return all those that have
			a seat available. 
		6. The search result will include both direct flights and flights with 
			one connection (i.e. two flights with a stop between)
		7. The result will include flight details (including flight number, source 
			and destination airport codes, depature and arrival times), the number
			of stops, the layover time for non-direct flights, the price and the 
			number of seats at that price 
		8. The result should be sorted based on price (from lowest to highest)
		9. The user should also have the option to sort the result based on the 
			number of connections (with direct flights listed first) as the primary 
			search criterion and the price as the secondary criterion

		'''

def search(src, dest, dep_date):
	print ("here")

def start_search():
	src = input("Enter source:")
	dest = input("Enter destination:")
	dep_date = input("Enter departure date:")

	check_airport(src,dest,dep_date)

def check_airport(src,dst,dep_date):
	src=src.upper()
	dst=dst.upper()
	query ="select flightno from flights where UPPER(src) = :src AND UPPER(dst) = :dst" 
	#query = "select city FROM airports WHERE UPPER(city) = :fuck" # WHERE city = :src"
	curs.execute(query, src = src, dst = dst)
	rows = curs.fetchall()
	'''if not rows:
	   print(src)
	   con.commit()
	   #q = "SELECT f.flightno FROM flights f, airports a1, airports a2 WHERE f.src = a1.acode AND f.dst = a2.acode AND UPPER(a1.city) = UPPER(:source)" 
	   #q = "select acode FROM airports WHERE UPPER(city) = :source"
	   curs.execute(q,source =src) 
	   rows = curs.fetchall() 
	   print(rows)
	   for row in rows: 
	       print(row[0])'''

	for row in rows:
		print(row[0])

	curs.close()
	con.close()
con = cx_Oracle.connect('lexie','santaclause1','gwynne.cs.ualberta.ca:1521/CRS')

curs = con.cursor()

start_search()
