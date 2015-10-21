import sys
import cx_Oracle
import getpass

def userLogin(curs):
	"Attempts to log user into system"
	#queryFile = open("loginSearch.sql", 'r')
	#queryStr = queryFile.read().replace('\n', ' ')
	#print(queryStr)
	#queryFile.close
	try:
		#curs.execute(queryStr, {'username':'UlaStyers@e.ca'})
		curs.execute("Select email from users where email = 'UlaStyers@e.ca'")
		rows = curs.fetchall()
		print(rows)
		
		curs.prepare("Select email from users where email = :username")
		curs.execute(None, {'username': 'UlaStyers@e.ca'})
		rows = curs.fetchall()
		print(rows)
	
	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "oracle message:", error.message)

	return

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
	sys.exit
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
