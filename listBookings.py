import sys
import cx_Oracle
import user
import clearScreen

def isInt(num):
	try:
		int(num)
		return(True)
	except ValueError:
		return(False)

def listSummaryBookings(curs, user1):
	
	clearScreen.clearScreen()
	try:
		queryFile = open('summaryBooking.sql', 'r')
		queryStr = queryFile.read().replace('\n', ' ')
		queryFile.close()
	
		queryStr = queryStr.replace(':email', user1.getEmail())

		curs.execute(queryStr)

		bookings = curs.fetchall()
		
		if len(bookings) > 0:
			print("Row    " + "TNO    "  + "Name" + " " * 16 + "Dep_Date     " + "Paid Price")
	
			i = 0
			for booking in bookings:
				line = (str(i) + " " * (7-len(str(i))) +
				str(booking[0]) + " " * (7-len(str(booking[0]))) + 
				str(booking[1]) +
				str(booking[2]) + " " * (13-len(str(booking[2]))) +
				str(booking[3]))
				
				print (line)

				i += 1	
	
			rowNum = input("Enter row number for more information. Blank entry will return to main menu.")
			while True:
				if rowNum == "":
					return()
					break
				elif isInt(rowNum):
					rowNum = int(rowNum)
					if rowNum >= 0 and rowNum < len(bookings):
						ticket = bookings[rowNum][0]
						listDetailBooking(curs, ticket)
						break
					else:
						print("Row Number out of range.")
						rowNum = input("Enter row number for more information. Blank entry will return to main menu.")

				else:
					print("Command not recognized.")
					rowNum = input("Enter row number for more information. Blank entry will return to main menu.")

		else:
			print("No Bookings Found. Press 'Enter' to continue.")
			input()
	
	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print (sys.stderr, "Oracle code:", error.code)
		print(sys.stderr, "Oracle message:", error.message)

	
	return()

def listDetailBooking(curs, ticket):
	input("Details of tno " + str(ticket))
	return()
