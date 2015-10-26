import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it

def createBooking( curs, thisUser, flightnum1, fare1, depDate1, flightnum2 = -1, fare2 = -1, depDate2 = -1):
	
	try:
		#begins new transaction
		curs.connection.begin()
		
		#get name
		passengerName = input("Your name [%s]: " % getpass.getuser())
		if not passengerName:
			passengerName=getpass.getuser()
		
		passengerEmail = thisUser.getEmail(thisUser)
		queryStr = "SELECT COUNT(*) FROM passengers p WHERE( p.name='passengerName' and p.email='passengerEmail')"
		queryStr = queryStr.replace("passengerName", passengerName)
		queryStr = queryStr.replace("passengerEmail", passengerEmail)
		
		curs.execute(queryStr)
		fetcher = curs.fetchAll()
		newUser = fetcher[0][0]
		
		if newUser==0:
			passengerCountry = input("Your country [%s]: " % getpass.getuser())
			if not passengerCountry:
				passengerCountry=getpass.getuser()
			
			queryStr = "INSERT INTO passengers VALUES ('passengerEmail', 'passongerName', 'passengerCountry')"
			queryStr = queryStr.replace("passengerName", passengerName)
			queryStr = queryStr.replace("passengerEmail", passengerEmail)
			queryStr = queryStr.replace("passengerCountry", passengerCountry)
			curs.execute(queryStr)
		
		#must create unique ticket number.
		#accidental duplicate handled by database exception
		curs.exucute("SELECT MAX(tno) FROM bookings")
		ticketNum = curs.fetch() + 1
		queryStr = "SELECT price FROM flight_fares WHERE fare=fare1"
		queryStr = queryStr.replace("fare1", fare1)
		curs.execute(queryStr)
		fetcher = curs.fetchAll()
		price = fetcher[0][0]
		
		#double check seats are still free!~~!!~!~~!!~!~~!!~~!~!~!~!~!~!~!~!~!~!~!
		#might want a try catch here(for detailed message) incase booking fails !~!~!~~!~!~!~!~!~!~!~!~!!
		#seat # is none, will be assigned when passengers check in at airport
		queryStr = "INSERT INTO bookings VALUES('ticketNum', 'flightnum1', 'fare1', 'depDate1', 'None')"
		queryStr = queryStr.replace("ticketNum", ticketNum)
		queryStr = queryStr.replace("flightNum1", flightNum1)
		queryStr = queryStr.replace("fare1", fare1)
		queryStr = queryStr.replace("depDate1", depDate1)
		queryStr = queryStr.replace("None", None)
		curs.execute(queryStr)
		
		
		if flightnum2 != -1 and fare2 != -1:
			queryStr = "SELECT price FROM flight_fares WHERE fare='fare2'"
			queryStr = queryStr.replace("fare2", fare2)
			curs.execute(queryStr)
			price += curs.fetch()
			queryStr = "INSERT INTO bookings VALUES('ticketNum', 'flightnum2', 'fare2', 'depDate2', 'None')"
			queryStr = queryStr.replace("ticketNum", ticketNum)
			queryStr = queryStr.replace("flightNum2", flightNum2)
			queryStr = queryStr.replace("fare2", fare2)
			queryStr = queryStr.replace("depDate2", depDate2)
			queryStr = queryStr.replace("None", None)
			curs.execute(queryStr)	
		
		queryStr = "INSERT INTO tickets VALUES('ticketNum', 'passengerName', 'passengerEmail', 'price'"
		queryStr = queryStr.replace("ticketNum", ticketNum)
		queryStr = queryStr.replace("pasengerName", passengerName)
		queryStr = queryStr.replace("passengerEmail", passengerEmail)
		queryStr = queryStr.replace("price", price)
		curs.execute(queryStr)
		
		curs.connection.commit()
		#assuming SQL exception if above failed
		print("Your booking was successful!\nHere is your ticket number: " + ticketNum)

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		curs.connetion.rollback() #rolls back transaction if fails
		print( "Something went wrong ")
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
