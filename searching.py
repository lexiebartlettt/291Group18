import cx_Oracle
import time
import math
import menu
import makeBooking
from operator import itemgetter

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


#gathers user input
def start_search(curs,user1):
	
	src = input("Enter source:")
	dest = input("Enter destination:")
	dep_date = input("Enter departure date (DD/MM/YYYY):")
	party_size = input("Enter how many people you are booking for:")
	round_trip = input("Would you like to book a round trip? (y/n)")

	srcCheck = checkCodes(src,curs)
	destCheck = checkCodes(dest,curs)

	if (srcCheck == False): 
		src = getAcode(src,curs)
		if (src == False):
			print("No Airport Matches")
			return

	if(destCheck == False): 
		dest = getAcode(dest,curs)
		if (dest == False):
			print("No Airport Matches")
			return

	#They want a round trip
	if (round_trip.upper() == 'Y'):
		return_date = input("Enter a return date (DD/MM/YYYY):")
		print("Trips: ")
		going = check_airport(src, dest, dep_date,curs)
		chooseSort(going,party_size)
		print("")
		print("Return Trips: ")
		coming = check_airport(dest, src, return_date,curs)
		chooseSort(coming,party_size)

		book = input("Would you like to book a flight? (y/n)")

		if (book.upper() == 'Y'): 
			going_option = input("Please enter option number for Flight\n")
			coming_option = input("Please enter option number for the Return Flight")
			
			going_option = int(going_option)
			coming_option = int(coming_option)

			if (going[going_option][7] == ""):
				makeBooking.createBooking(curs, user1,going[going_option][0], going[going_option][12], str(going[going_option][3]),-1, -1)
			else:
				makeBooking.createBooking(curs,user1,going[going_option][0], going[going_option][12], str(going[going_option][3]), going[going_option][10],going[going_option][11])
			

			if (coming[coming_option][7] == ""):
				makeBooking.createBooking(curs, user1,coming[coming_option][0], coming[coming_option][12], str(coming[coming_option][3]),-1, -1)
			else:
				makeBooking.createBooking(curs,user1,coming[coming_option][0], coming[coming_option][12], str(coming[coming_option][3]), coming[coming_option][10],coming[coming_option][11])
			
		else: 
			return

	#They don't want a round trip
	elif (round_trip.upper() == 'N'):
		all_flights = check_airport(src,dest,dep_date,curs)
		chooseSort(all_flights, party_size)
		book = input("Would you like to book a flight? (y/n)")
		option = input("Please enter option number for Flight\n")
		option = int(option)
		if (book.upper() == 'Y'): 
			
			if (all_flights[option][7] == ""):
				makeBooking.createBooking(curs, user1,all_flights[option][0], all_flights[option][12], str(all_flights[option][3]),-1, -1)
			else:
				makeBooking.createBooking(curs,user1,all_flights[option][0], all_flights[option][12], str(all_flights[option][3]), all_flights[option][10],all_flights[option][11])
		else: 
			print("Go to menu here")

	#They suck at entering letters
	else: 
		print("Invalid Option")
		start_search(curs,user1)



#SQL queries for airport searches
def check_airport(src,dst,dep_date, curs):
	src=src.upper()
	dst=dst.upper()

	query = "select flightno, src, dst, dep_time, arr_time, price, seats, fare FROM available_flights  WHERE to_char(dep_date,'DD/MM/YYYY')=:depature_date AND src = :src AND dst = :dst ORDER BY price" # WHERE city = :src"
	curs.execute(query,depature_date=dep_date, src = src, dst = dst)
	rows = curs.fetchall()
	x = 0
	all_flights = []
	if rows: 

		for row in rows: 
			current = [0,0,0,0,0,0,0,0,0,0,0,0,0]
			#flight number
			current[0] = row[0]

			#src 
			current[1] = row[1]

			#dst
			current[2] = row[2]

			#dep_time
			current[3] = row[3]

			#arr_time 
			current[4] = row[4]

			#price
			current[5] = row[5]

			#seats 
			current[6] = row[6]

			#the next 3 are null because no connection 
			current[7] = ""
			current[8] = ""
			current[9] = ""
			current[10] = ""
			current[11] = "" 

			#fare type
			current[12] = row[7]


			all_flights.append(current)


	query = "select a1.flightno, a1.src, a2.dst, a1.dep_time, a2.arr_time, a1.price, a2.price, a1.seats, a2.seats, a1.arr_time, a2.dep_time, a1.dst, a2.flightno, a1.fare, a2.fare  from available_flights a1, available_flights a2 WHERE a1.src = :src AND a2.dst = :dst AND to_char(a2.dep_date,'DD/MM/YYYY')=:dep_date AND a1.dst = a2.src AND a1.dep_date = a2.dep_date ORDER BY (a1.price+a2.price)"
	curs.execute(query,src = src,dst = dst, dep_date = dep_date)
	rows = curs.fetchall()

	if rows: 
		for row in rows: 
			current = [0,0,0,0,0,0,0,0,0,0,0,0,0]
			#flight number
			current[0] = row[0]

			#src 
			current[1] = row[1]

			#dst
			current[2] = row[2]

			#dep_time
			current[3] = row[3]

			#arr_time 
			current[4] = row[4]

			#price
			current[5] = row[5]+row[6]

			#seats 
			current[6] = abs(row[7]-row[8])

			#connection?	
			current[7]=1 

			#Where is the connection
			current[8] = row[11]

			#Layover time
			current[9] = row[9] - row[10]

			#connection flightno 
			current[10] = row[12] 

			#fare type #2 
			current[11] = row[13]

			#fare type #1 
			current[12] = row[14]

			all_flights.append(current)

	return all_flights

def getAcode(city, curs): 
	city = city.upper()
	results = []

	query = "select acode, city, name from airports WHERE UPPER(city) LIKE '%:city%'"
	query = query.replace(":city",city)	
	curs.execute(query)
	rows = curs.fetchall()
	for row in rows: 
		results.append(row)

	query = "select acode, city, name from airports WHERE UPPER(name) LIKE '%:name%'"
	query = query.replace(":name",city)	
	curs.execute(query)
	rows = curs.fetchall()

	for row in rows: 
		results.append(row)

	if not results:
		return False
	else:
		for r in results:
			print("") 
			print("Airport Code: " + r[0])
			print("City:" + r[1])
			print("Airport Name:" + r[2])
		city = input("Enter Airport Code: ")
		return city



def checkCodes(code, curs):
	code = code.upper()
	query = "select acode from airports WHERE UPPER(acode) =':code'"
	query = query.replace(":code",code)
	curs.execute(query)
	rows = curs.fetchall()

	if not rows: 
		return False
	else: 
		return True

def print_flights(flights, party_size):
	
	x = 0
	for flight in flights: 
		if(int(party_size) <= flight[6]):
			print("Option:" + str(x))
			print("Flight Number: " + str(flight[0]))
			print("From: " + str(flight[1]) + " to " + str(flight[2]))
			print("Departure Time:" + str(flight[3]))
			print("Arrival Time: " + str(flight[4]))
			print("Price: " + str(flight[5]) + " Fare Type: " + str(flight[12]))
			print("Seats Available: " + str(flight[6]))

			if flight[7] == 1: 
				print("This flight has a connection in " + str(flight[8]))
				print("Connection Flight Number: " + str(flight[10]))
				print("Layover Time: "+ str(flight[9]))
			else: 
				print("This is a direct flight")
			print(" ")
		else:	
			print("Flight " + flight[0] + " is full")
			print("")
		x+=1



def chooseSort(flights, party_size):
	flights1 = sort_by_price(flights)
	if(len(flights)==0): 
		print("No flights matching your criteria")
		print("")
		#This is where the city 
	else:
		print_flights(flights1, party_size)
		sortby = input("Would you like to sort by number of connections (y/n):")
		if (sortby.upper() == 'Y'):
			print_flights(flights,party_size)
			return
		elif (sortby.upper() == 'N'):
			return
		else: 
			print("Invalid Option")
			return

def sort_by_price(flights):
	sorted(flights,key=itemgetter(5))
	return flights


