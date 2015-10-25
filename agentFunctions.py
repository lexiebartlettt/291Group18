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

def isTime(depTime):
	if len(depTime) != 5:
		print("Input not recogonised.")
		return(False)
	elif isInt(depTime[0:2]) and isInt(depTime[3:]) and depTime[2] == ":":
		if int(depTime[0:2]) >= 0 and int(depTime[0:2]) <= 23:
			if int(depTime[3:]) >= 0 and int(depTime[3:]) <= 59:
				return (True)
			else:
				print("Invalid Time")
				return(False)
		else:
			print("Invalid Time")	
			return(False)
	else:
		print("Input not recogonised.")
		return(False)
	return(False)

def recordDep(curs):
	#clearScreen.clearScreen()
	flightno = input("Please Enter a flight number: ")
	queryStr = "Select flightno, to_char(dep_date, 'dd-mon-yy') from sch_flights where flightno = " +"'"+flightno+"'"
	
	try:
		curs.execute(queryStr)

		flightDates = curs.fetchall()

		if len(flightDates) == 0:
			clearScreen.clearScreen()
			print("Flight " + flightno + " not found")
			recordDep(curs)
			return()

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
					clearScreen.clearScreen()
					print("Updating Departure Time for: " + flightDates[rowNum][0] + " on " + flightDates[rowNum][1]) 
					while True:
						depTime = input("Input departure time in following format '00:00'\n")
						if isTime(depTime):
							updateDepTime(curs, flightDates[rowNum][0], depTime, flightDates[rowNum][1])
							#print("Winner winner")
							return()
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

def updateDepTime(curs, flight, depTime, fDate):
	try:
		queryStr = "Update sch_flights set act_dep_time = to_date(':depTime', 'hh24:mi') where flightno = ':flight' and dep_date = to_date(':fDate', 'dd-mon-yy')"
		queryStr = queryStr.replace(":depTime", depTime)
		queryStr = queryStr.replace(":flight", flight)
		queryStr = queryStr.replace(":fDate", fDate)
		
		curs.execute(queryStr)
		curs.connection.commit()

		print("Departure time updated. Press 'Enter' to return to main menu.")
		input()

		clearScreen.clearScreen()

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print (sys.stderr, "Oracle code:", error.code)
		print(sys.stderr, "Oracle message:", error.message)
		input()


def recordArr(curs):
	#clearScreen.clearScreen()
	flightno = input("Please Enter a flight number: ")
	queryStr = "Select flightno, to_char(dep_date, 'dd-mon-yy') from sch_flights where flightno = " +"'"+flightno+"'"
	
	try:
		curs.execute(queryStr)

		flightDates = curs.fetchall()

		if len(flightDates) == 0:
			clearScreen.clearScreen()
			print("Flight " + flightno + " not found")
			recordDep(curs)
			return()

		print("Row   " + "Flightno    " + "Date")
	
		i = 0
		for flightDate in flightDates:
			print(str(i) + (" " * (6-len(str(i)))) +
			flightDate[0] + (" " * (12-len(flightno))) +
			flightDate[1])
			i += 1
	
		rowNum = input("Enter row number to record arrival time. Blank entry will return to main menu.\n")
		while True:
			if rowNum == "":
				return()
				break
			elif isInt(rowNum):
				rowNum = int(rowNum)
				if rowNum >= 0 and rowNum < len(flightDates):
					clearScreen.clearScreen()
					print("Updating arrival Time for: " + flightDates[rowNum][0] + " on " + flightDates[rowNum][1]) 
					while True:
						arrTime = input("Input arrival time in following format '00:00'\n")
						if isTime(arrTime):
							updateArrTime(curs, flightDates[rowNum][0], arrTime, flightDates[rowNum][1])
							return()
				else:
					print("Row Number out of range.")
					rowNum = input("Enter row number to record arrival time. Blank entry will return to main menu.\n")
			else:
				print("Command not recognized.")
				rowNum = input("Enter row number to record arrival time. Blank entry will return to main menu.\n")
		#input()

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print (sys.stderr, "Oracle code:", error.code)
		print(sys.stderr, "Oracle message:", error.message)
		input()

	return()



def updateArrTime(curs, flight, arrTime, fDate):
	try:
		queryStr = "Update sch_flights set act_arr_time = to_date(':arrTime', 'hh24:mi') where flightno = ':flight' and dep_date = to_date(':fDate', 'dd-mon-yy')"
		queryStr = queryStr.replace(":arrTime", arrTime)
		queryStr = queryStr.replace(":flight", flight)
		queryStr = queryStr.replace(":fDate", fDate)
		
		curs.execute(queryStr)
		curs.connection.commit()

		print("Arrival time updated. Press 'Enter' to return to main menu.")
		input()

		clearScreen.clearScreen()

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print (sys.stderr, "Oracle code:", error.code)
		print(sys.stderr, "Oracle message:", error.message)
		input()
