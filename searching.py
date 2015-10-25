import cx_Oracle
import time
import math
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

def search(src, dest, dep_date):
	print ("here")

def start_search():
	src = input("Enter source:")
	dest = input("Enter destination:")
	dep_date = input("Enter departure date (DD/MM/YYYY):")

	check_airport(src,dest,dep_date)

def check_airport(src,dst,dep_date):
	src=src.upper()
	dst=dst.upper()
	#query ="select flightno from flights where UPPER(src) = :src AND UPPER(dst) = :dst" 
	query = "select flightno, src, dst, dep_time, arr_time, price, seats FROM available_flights  WHERE to_char(dep_date,'DD/MM/YYYY')=:depature_date AND src = :src AND dst = :dst ORDER BY price" # WHERE city = :src"
	curs.execute(query,depature_date=dep_date, src = src, dst = dst)
	rows = curs.fetchall()
	x = 0
	all_flights = []
	if rows: 

		for row in rows: 
			current = [0,0,0,0,0,0,0,0,0,0]
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

			all_flights.append(current)


	query = "select a1.flightno, a1.src, a2.dst, a1.dep_time, a2.arr_time, a1.price, a2.price, a1.seats, a2.seats, a1.arr_time, a2.dep_time, a1.dst  from available_flights a1, available_flights a2 WHERE a1.src = :src AND a2.dst = :dst AND to_char(a2.dep_date,'DD/MM/YYYY')=:dep_date AND a1.dst = a2.src AND a1.dep_date = a2.dep_date ORDER BY (a1.price+a2.price)"
	curs.execute(query,src = src,dst = dst, dep_date = dep_date)
	rows = curs.fetchall()

	if rows: 
		for row in rows: 
			current = [0,0,0,0,0,0,0,0,0,0]
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

			all_flights.append(current)

	chooseSort(all_flights)

	curs.close()
	con.close()

def print_flights(flights):
	
	for flight in flights: 
		print("Flight Number: " + str(flight[0]))
		print("From: " + str(flight[1]) + " to " + str(flight[2]))
		print("Departure Time:" + str(flight[3]))
		print("Arrival Time: " + str(flight[4]))
		print("Price: " + str(flight[5]))
		print("Seats Available: " + str(flight[6]))

		if flight[7] == 1: 
			print("This flight has a connection in " + str(flight[8]))
			print("Layover Time: "+ str(flight[9]))
		else: 
			print("This is a direct flight")
		print(" ")



def chooseSort(flights):
	flights1 = sort_by_price(flights)
	print_flights(flights1)

	sortby = input("Would you like to sort by number of connections (y/n):")
	if (sortby.upper() == 'Y'):
		print_flights(flights)
	elif (sortby.upper == 'N'):
		print("Return to menu here")
	else: 
		print("Invalid Option")

def sort_by_price(flights):
	sorted(flights,key=itemgetter(5))
	return flights


if __name__ == '__main__':	
	con = cx_Oracle.connect('lexie','santaclause1','gwynne.cs.ualberta.ca:1521/CRS')

	curs = con.cursor()

	start_search()
