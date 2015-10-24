# INCOMPLETE

import sys
import cx_Oracle # the package used for accessing Oracle in Python
import getpass # the package for getting password from user without displaying it



#connect to database
	# get username
	user = input("Username [%s]: " % getpass.getuser())
	if not user:
    		user=getpass.getuser()
	
	# get password
	pw = getpass.getpass()

	# The URL we are connnecting to
	conString=''+user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'



def createBooking( flightnum1, flightnum2 = -1, thisUser):
	
	# SQL statement to execute
	createStr = ("create table TOFFEES "
	"(T_NAME VARCHAR(32) PRIMARY KEY, SUP_ID INTEGER, PRICE FLOAT, SALES INTEGER, TOTAL INTEGER)")
	
	try:
		# Establish a connection in Python
		connection = cx_Oracle.connect(conString)

		# create a cursor 
		curs = connection.cursor()
		curs.execute("drop table toffees")
		curs.execute(createStr)
		
		#get name
		passengerName = input("Your name [%s]: " % getpass.getuser())
		if not passengerName:
    		passengerName=getpass.getuser()

    		checkPassStr = ("SELECT COUNT(*) FROM passengers p WHERE p.name=passengerName", passengerName=passengerName)
    		
    		curs.execute(checkPassStr)
    		newUser = curs.fetch()
    		if newUser=0:
    			#get country!~~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~! thisUser.getEmail(thisUser)
    			curs.execute("INSERT INTO #FINISH!~~!~!~!!~!!~!~!~!~!~!~!~~!!~~!~!
    		
    				

    	

		#OLD BELOW
		#OLD BELOW
		#OLD BELOW
		data = [('Quadbury', 101, 7.99, 0, 0), ('Smarties',102,6.99,1,2)]

		curs.bindarraysize = 2
		curs.setinputsizes(32, int, float, int, int)
		curs.executemany("INSERT INTO TOFFEES(T_NAME, SUP_ID, PRICE, SALES, TOTAL) "
                                    "VALUES (:1, :2, :3, :4, :5)", data)
		#curs.execute("INSERT INTO TOFFEES "
		#"VALUES('Quadbury',101,7.99,0,0)")
		connection.commit()
		
		# executing a query
		curs.execute("SELECT * from TOFFEES")
		# get all data and print it
		rows = curs.fetchall()
		for row in rows:
			print(row)
		
		# getting metadata
		rows = curs.description
		columnCount = len(rows)
		# display column names and type
		# (name, type, display_size,internal_size,precision,scale,null_ok)
		for row in rows:
			print(row[0]," ",row[1])

		# close the connection
		curs.close()
		connection.close()

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
		
# code for testing?
if __name__ == "__main__":
    createBooking(AC499)
