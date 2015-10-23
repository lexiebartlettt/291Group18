import sys
import cx_Oracle
from login import connect


def createView(curs, filename, viewName):
	viewFile = open(filename,'r')
	viewStr = viewFile.read().replace('\n', ' ')
	viewFile.close()

	try:
		curs.execute("Drop view " + viewName)
		curs.connection.commit()		

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		if not (error.code == 942 or error.code =='942'): #error code 942 = view does not exist, no error, do nothing
			print( sys.stderr, "Oracle code:", error.code)
			print( sys.stderr, "Oracle message:", error.message)
	
	try:
		curs.execute(viewStr)
		curs.connection.commit()		
		print("View created: " + viewName)

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)


if __name__ == '__main__':
	curs = connect()
	createView(curs, "availableFlights.sql", "available_flights")
	createView(curs, "goodConnections.sql", "good_connections")
	createView(curs, "allFlights.sql", "allFlights")
