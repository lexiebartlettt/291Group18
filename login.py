import sys
import cx_Oracle
import getpass
import os
import clearScreen
import user
import menu
import createViews

def userLogin(curs):
	"Attempts to log user into system"
	queryFile = open("loginSearch.sql", 'r')
	queryStr = queryFile.read().replace('\n', ' ')
	queryFile.close()
	try:
		
		clearScreen.clearScreen()
		
		uname = input("Please enter username: ")
		pwd = getpass.getpass()
		
		uname = "'" + uname + "'"
		pwd = "'" + pwd + "'"
		
		queryStr = queryStr.replace(":username", uname)
		queryStr = queryStr.replace(":pwd", pwd)
		
		
		curs.execute(queryStr)
		
		rows = curs.fetchall()
		result = rows[0][0]

		#check if user is agent
		curs.execute("Select count(*) from airline_agents where email = " + uname)
		isAgentRows = curs.fetchall()
		isAgentResult = isAgentRows[0][0]
		 
		if isAgentResult == 1:
			isAgent = True
		elif isAgentResult == 0:
			isAgent = False
		else:
			print ("Unforseen Error (agent)")
			print( "Result = " + str(isAgentResult))
			for row in isAgentRows:
				print(row)
			sys.exit()

		#print("Agent status: " + str(isAgent))
	
		if result == 1:
			print("Login Successful")
			user1 = user.User(uname, isAgent)
			menu.displayMenu(curs, user1)
			#print("Do menu function")
			sys.exit()
		elif result == 0:
			print("Login Unsuccessful")
			displayLoginScreen(curs)
			sys.exit()
		else:
			print ("Unforseen Error")
			print( "Result = " + str(result))
			for row in rows:
				print(row)
			sys.exit()
		
	
	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)


def connect():

	user = input("Username [%s]: " % getpass.getuser())
	if not user:
    		user=getpass.getuser()

	pw = getpass.getpass()

	connStr = ''+user+'/' + pw + '@gwynne.cs.ualberta.ca:1521/CRS'

	try:
		connection = cx_Oracle.connect(connStr)
		curs = connection.cursor()
	
	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
		print("Connection Failed. Exiting Program")
		sys.exit()
		
		
	createViews.createView(curs, "availableFlights.sql", "available_flights")
	createViews.createView(curs, "goodConnections.sql", "good_connections")
	createViews.createView(curs, "allFlights.sql", "allFlights")
	
	return(curs)

def displayLoginScreen(curs):	
	try:
		print("Welcome to group 18's airline management system.")
		print("Type Login, Register or Exit to continue.")
	
		userInput = input()

		while True:
			if userInput.strip().lower() in ('login', 'log', 'l'):
				#print("Logging in.")
				userLogin(curs)
				break
			elif userInput.strip().lower() in ('register', 'reg', 'r'):
				#print("Registering")
				registerUser(curs)
				break
			elif userInput.strip().lower() in ('exit', 'e'):
				print("Goodbye.")
				sys.exit
				break #reduanant but just in case...
			else:
				print("Input not recognised.")
				print("Type Login, Register or Exit to continue.")
				userInput = input()
	
		
	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
	
	return()

def registerUser(curs):

	try:
		
		queryStr = "Insert into users values (:username, :pwd, NULL)" 
		uname = input("Please enter username: ")
		print("Please enter a password below, max 4 characters.")
		pwd = getpass.getpass()

		while len(pwd) > 4 or len(pwd) < 1:
			print("Invalid password lenght")
			pwd = getpass.getpass()
		
		uname = "'" + uname + "'"
		pwd = "'" + pwd + "'"
		
		queryStr = queryStr.replace(":username", uname)
		queryStr = queryStr.replace(":pwd", pwd)

		curs.connection.begin()		
		curs.execute(queryStr)
		curs.connection.commit()
		
		isAgent = False
		user1 = user.User(uname, isAgent)
		menu.displayMenu(curs, user1)
		sys.exit()

	except cx_Oracle.DatabaseError as exc:
		curs.connection.rollback()		
		error, = exc.args
		if error.code == 1:
			print("Username already taken. Please try again")
			registerUser(curs)
		else:
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message)
		
if __name__ == '__main__':
	curs = connect()
	clearScreen.clearScreen()
	displayLoginScreen(curs)
	
