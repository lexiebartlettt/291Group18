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

def recordDep(curs):
	flightno = input("Please Enter a flight number: ")
	queryStr = "Select flightno, to_char(dep_date, 'dd-mon-yy') from sch_flights where flightno = " +"'"+flightno+"'"
	
	try:
		curs.execute(queryStr)

		flightDates = curs.fetchall()

		print("Row   " + "Flightno    " + "Date")
	
		i = 0
		for flightDate in flightDates:
			print(str(i) + (" " * (6-len(str(i)))) +
			flightDate[0] + (" " * (12-len(flightno))) +
			flightDate[1])
			i += 1
	
		rowNum = input("Enter row number to record departure time. Blank entry will return to main menu.\n")
		while True:
			if rowNum == "":
				return()
				break
			elif isInt(rowNum):
				rowNum = int(rowNum)
				if rowNum >= 0 and rowNum < len(flightDates):
					while True:
						depTime = input("Input departure time in following format '00:00'\n")
						if len(depTime) != 5:
							print("Input not recogonised.")
							depTime = input("Input departure time in following format '00:00'\n")
						elif isInt(depTime[0:2]) and isInt(depTime[3:]) and depTime[2] == ":":
							if int(depTime[0:2]) >= 0 and int(depTime[0:2]) <= 23:
								if int(depTime[3:]) >= 0 and int(depTime[3:]) <= 59:
									print("You win")
									break
								else:
									print("Invalid Time")
							else:
								print("Invalid Time")	
								depTime = input("Input departure time in following format '00:00'\n")
							
						else:
							print("Input not recogonised.")
							depTime = input("Input departure time in following format '00:00'\n")
						
					break
				else:
					print("Row Number out of range.")
					rowNum = input("Enter row number to record departure time. Blank entry will return to main menu.\n")
			else:
				print("Command not recognized.")
				rowNum = input("Enter row number to record departure time. Blank entry will return to main menu.\n")
		#input()

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print (sys.stderr, "Oracle code:", error.code)
		print(sys.stderr, "Oracle message:", error.message)
		input()

	return()

'''def listSummaryBookings(curs, user1):
	
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

		input("Press 'Enter' to return.")
	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print (sys.stderr, "Oracle code:", error.code)
		print(sys.stderr, "Oracle message:", error.message)
		input()
		
	return()
'''


