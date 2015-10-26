import sys
import clearScreen
import user
import listBookings
import agentFunctions
import searching
import booking


def giveOptions(user1):
	
	print("Welcome. Please choose one of the following options.")
	print("Type 'Search' to search for a flight. ")
	print("Type 'Book' to make a booking.")
	print("Type 'List' to list existing bookings.")
	print("Type 'Logout' to logout.")

	if user1.isAgent():
		print( "\n Agent Options")
		print("Type 'Dep' to record a flight departure")
		print("Type 'Arr' to record a flight arrival")
	return()

def logout(curs, user1):
	try:
	
		queryStr = "Update users set last_login = sysdate where email = :username"
		queryStr = queryStr.replace(":username", user1.getEmail())
	
		curs.execute(queryStr)
		curs.connection.commit()
	
	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print (sys.stderr, "Oracle code:", error.code)
		print (sys.stderr, "Oracle Message:", error.message)
	

def displayMenu(curs, user1):
	
	clearScreen.clearScreen()	
	while True:
		giveOptions(user1)
		userInput = input()
		if userInput.strip().lower()  == 'search':
			searching.startSearch(curs)
			clearScreen.clearScreen()	

		elif userInput.strip().lower() == 'book':
			clearScreen.clearScreen()
			flightno = input("Please enter flight number.\n")
			fareType = input("Please enter fare type. \n")
			dep_date = input("Please enter departure date in the following format: 'dd/mm/yy' \n")
			print("Would you like to book a connection?")
			connect = input()

			flight2 = -1
			far2 = -1
			
			if connect.strip().lower() in ('y', 'yes'):
				flight2 = input("Please enter second flight number. \n")
				fare2 = input("Please enter second flight fare type. \n")
						
			booking.createBooking(curs, user1, flightno, fareType, flight2, fare2)
			clearScreen.clearScreen()	
		elif userInput.strip().lower() == 'list':
			listBookings.listSummaryBookings(curs, user1)
			clearScreen.clearScreen()	
		elif userInput.strip().lower() == 'logout':
			print("Logging out.")
			logout(curs, user1)
			sys.exit()
		elif userInput.strip().lower() == 'dep':
			if user1.isAgent():
				agentFunctions.recordDep(curs)
			else:
				clearScreen.clearScreen()
				print("Action Unauthorized")
		elif userInput.strip().lower() == 'arr':
			if user1.isAgent():
				agentFunctions.recordArr(curs)
			else:
				clearScreen.clearScreen()
				print("Action Unauthorized")
		else:
			clearScreen.clearScreen()
			print("Command not recognised.\n")
			#break
			
		
	return()
