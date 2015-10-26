import sys
import cx_Oracle
import user
import clearScreen
import cancelBooking

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
	
			rowNum = input("Enter row number for more information. Blank entry will return to main menu.  ")
			while True:
				if rowNum == "":
					return()
					break
				elif isInt(rowNum):
					rowNum = int(rowNum)
					if rowNum >= 0 and rowNum < len(bookings):
						ticket = bookings[rowNum][0]
						flightno = bookings[rowNum][4]
						dep_date = bookings[rowNum][2]
						listDetailBooking(curs, ticket, flightno, dep_date)
						break
					else:
						print("Row Number out of range.")
						rowNum = input("Enter row number for more information. Blank entry will return to main menu.  ")

				else:
					print("Command not recognized.")
					rowNum = input("Enter row number for more information. Blank entry will return to main menu.  ")

		else:
			print("No Bookings Found. Press 'Enter' to continue.")
			input()
	
	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print (sys.stderr, "Oracle code:", error.code)
		print(sys.stderr, "Oracle message:", error.message)
		input()

	
	return()

def listDetailBooking(curs, ticket, flightno, dep_date):
	#input("Details of tno " + str(ticket) + " flight no " + str(flightno) + " dep_date " + str(dep_date))

	clearScreen.clearScreen()
	try:
		queryFile = open('detailedBooking.sql', 'r')
		queryStr = queryFile.read().replace('\n', ' ')
		queryFile.close()
	
		queryStr = queryStr.replace(':ticket', str(ticket))
		queryStr = queryStr.replace(':flight', "'"+str(flightno)+"'")
		queryStr = queryStr.replace(':depdate', "'"+str(dep_date)+"'")

		#input(queryStr)
		curs.execute(queryStr)

		bookings = curs.fetchall()
		columns = curs.description
		
		for i in range(0,len(columns)-1):
			item = str(columns[i][0]) + " : " + str(bookings[0][i])
			print(item)

		cancel = input("Type 'Cancel' to cancel this booking. Press 'Enter' to return to main menu.\n")

		if cancel.strip().lower() == 'cancel':
			ticketno = bookings[0][0]
			flightno = bookings[0][2]
			dep_date = bookings[0][7]
			fare = bookings[0][6]	
			cancelBooking.cancelBooking(ticketno, flightno, dep_date, fare,  curs)


	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print (sys.stderr, "Oracle code:", error.code)
		print(sys.stderr, "Oracle message:", error.message)
		input()
		
	return()
