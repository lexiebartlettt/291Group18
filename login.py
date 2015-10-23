import sys
import cx_Oracle
import getpass
import os
import clearScreen

def userLogin(curs):
	"Attempts to log user into system"
	queryFile = open("loginSearch.sql", 'r')
	queryStr = queryFile.read().replace('\n', ' ')
	queryFile.close()
	try:
		
		clearScreen()
		
		uname = input("Please enter username: ")
		pwd = getpass.getpass()
		
		uname = "'" + uname + "'"
		pwd = "'" + pwd + "'"
		
		queryStr = queryStr.replace(":username", uname)
		queryStr = queryStr.replace(":pwd", pwd)
		
		
		curs.execute(queryStr)
		
		rows = curs.fetchall()
		result = rows[0][0]

		if result == 1:
			print("Login Successful")
			#openMenu()
			print("Do menu function")
		elif result == 0:
			print("Login Unsuccessful")
			#initialLogin()
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
		print( sys.stderr, "oracle message:", error.message)

	return

def connect():
	user=getpass.getuser()
	pw = getpass.getpass()

	connStr = ''+user+'/' + pw + '@gwynne.cs.ualberta.ca:1521/CRS'

	try:
		connection = cx_Oracle.connect(connStr)
		curs = connection.cursor()
	
	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "oracle message:", error.message)
		print("Connection Failed. Exiting Program")
		sys.exit()
	return(curs)

def displayLoginScreen(curs):	
	try:
		print("Welcome to group 18's airline management system.")
		print("Type Login, Register or Exit to continue.")
	
		userInput = input()

		while True:
			if userInput.strip().lower() in ('login', 'log', 'l'):
				print("Logging in.")
				userLogin(curs)
			
				break
			elif userInput.strip().lower() in ('register', 'reg', 'r'):
				print("Registering")
				#registerUser()
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
		print( sys.stderr, "oracle message:", error.message)
	
	return()

if __name__ == '__main__':
	curs = connect()
	displayLoginScreen(curs)
	
