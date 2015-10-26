import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it
import user

def createBooking( curs, thisUser, flightnum1, fare1, depDate, flightnum2 = -1, fare2 = -1):
	
	try:
		#begins new transaction
		curs.connection.begin()
		
		#get name
		passengerName = input("Your name [%s]: " % getpass.getuser())
		if not passengerName:
			passengerName=getpass.getuser()
		
		passengerEmail = thisUser.getEmail()
		queryStr = "SELECT COUNT(*) FROM passengers p WHERE( p.name='passengerName' and p.email='passengerEmail')"
		queryStr = queryStr.replace("passengerName", passengerName)
		queryStr = queryStr.replace("passengerEmail", passengerEmail)
		
		curs.execute(queryStr)
		fetcher = curs.fetchall()
		newUser = fetcher[0][0]
		
		if newUser==0:
			passengerCountry = input("Your country [%s]: " % getpass.getuser())
			#if not passengerCountry:
				#passengerCountry=getpass.getuser()
			
			queryStr = "INSERT INTO passengers VALUES ('passengerEmail', 'passengerName', 'passengerCountry')"
			queryStr = queryStr.replace("passengerName", passengerName)
			queryStr = queryStr.replace("passengerEmail", passengerEmail)
			queryStr = queryStr.replace("passengerCountry", passengerCountry)
			curs.execute(queryStr)
			#curs.connection.commit()
			#curs.connection.begin()
		
		#must create unique ticket number.
		#accidental duplicate handled by database exception
		curs.execute("SELECT MAX(tno) FROM tickets")
		maxNum = curs.fetchall()		
		ticketNum = maxNum[0][0] + 1
		queryStr = "SELECT price FROM flight_fares WHERE fare='fare1' and flightno='flightnum1'"
		queryStr = queryStr.replace("fare1", fare1)
		queryStr = queryStr.replace("flightnum1", flightnum1)
		curs.execute(queryStr)
		fetcher = curs.fetchall()
		price = fetcher[0][0]
		
		queryStr = "Insert into tickets values(ticketno, 'pname', 'pemail', paid)"
		queryStr = queryStr.replace("ticketno", str(ticketNum))
		queryStr = queryStr.replace("pname", passengerName)
		queryStr = queryStr.replace("pemail", passengerEmail)
		queryStr = queryStr.replace("paid", str(price))
		
		#print(queryStr)
		curs.execute(queryStr)
		#curs.connection.commit()

		#double check seats are still free!~~!!~!~~!!~!~~!!~~!~!~!~!~!~!~!~!~!~!~!
		#might want a try catch here(for detailed message) incase booking fails !~!~!~~!~!~!~!~!~!~!~!~!!
		#seat # is none, will be assigned when passengers check in at airport
		queryStr = "INSERT INTO bookings VALUES(ticketNum, 'flightnum1', 'fare1', to_date('depDate', 'dd/mm/yy'), NULL)"
		queryStr = queryStr.replace("ticketNum", str(ticketNum))
		queryStr = queryStr.replace("flightnum1", flightnum1)
		queryStr = queryStr.replace("fare1", fare1)
		queryStr = queryStr.replace("depDate", depDate)
		#queryStr = queryStr.replace("None", None)
		curs.execute(queryStr)
		
		
		if flightnum2 != -1 and fare2 != -1:
			queryStr = "SELECT price FROM flight_fares WHERE fare='fare2' and flightno='flightnum2'"
			queryStr = queryStr.replace("fare2", fare2)
			queryStr = queryStr.replace("flightnum2", flightnum2)
			curs.execute(queryStr)
			fetcher = curs.fetchall()
			price2 = fetcher[0][0]

			print (str(price2))

			queryStr = "INSERT INTO bookings VALUES(ticketNum, 'flightnum2', 'fare2', to_date('depDate', 'dd/mm/yy'), NULL)"
			queryStr = queryStr.replace("ticketNum", str(ticketNum))
			queryStr = queryStr.replace("flightnum2", flightnum2)
			queryStr = queryStr.replace("fare2", fare2)
			queryStr = queryStr.replace("depDate", depDate)
			curs.execute(queryStr)	
		
		'''queryStr = "INSERT INTO tickets VALUES(ticketNum, 'passengerName', 'passengerEmail', 'price')"
		queryStr = queryStr.replace("ticketNum", str(ticketNum))
		queryStr = queryStr.replace("pasengerName", passengerName)
		queryStr = queryStr.replace("passengerEmail", passengerEmail)
		queryStr = queryStr.replace("price", str(price))
		curs.execute(queryStr)'''

		queryStr = "UPDATE tickets set paid_price = totPrice where tno = ticketNum"
		queryStr = queryStr.replace("totPrice", str(price+price2))
		queryStr = queryStr.replace("ticketNum", str(ticketNum))
		curs.execute(queryStr)
		
		curs.connection.commit()
		#assuming SQL exception if above failed
		print("Your booking was successful!\nHere is your ticket number: " + str(ticketNum))

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		curs.connection.rollback() #rolls back transaction if fails
		print( "Something went wrong ")
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)



if __name__ == '__main__':
	user2=getpass.getuser()
	pw = getpass.getpass()

	connStr = ''+user2+'/' + pw + '@gwynne.cs.ualberta.ca:1521/CRS'

	try:
		connection = cx_Oracle.connect(connStr)
		curs = connection.cursor()
	
	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
		print("Connection Failed. Exiting Program")
		sys.exit()
	'''
	flightno = input("Please enter flight number.")
	fareType = input("Please enter fare type.")
	dep_date = input("Please enter departure date in the following format: 'dd/mm/yy' \n")
	'''
	print("Would you like to book a connection?")
	connect = input()
	
	
	flight2 = -1
	fare2 = -1
	
			
	if connect.strip().lower() in ('y', 'yes'):
		flight2 = input("Please enter second flight number. \n")
		fare2 = input("Please enter second flight fare type. \n")

	uname = "brad@mail.com"	
	user1 = user.User(uname, False)					
	createBooking(curs, user1, 'AC343', 'F', '13/09/2015', flight2, fare2)





