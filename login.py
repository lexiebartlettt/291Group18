import sys
import cx_Oracle
import getpass

user=getpass.getuser()
pw = getpass.getpass()

connStr = ''+user+'/' + pw + '@gwynne.cs.ualberta.ca:1521/CRS'

try:
	connection = cx_Oracle.connect(connStr)
	curs = connection.cursor()

except:
	print("error")

curs.execute('Drop table temp')
connection.commit()

try:
	curs.execute('Create table temp (var1 INTEGER)')
	connection.commit()
	
except cx_Oracle.DatabaseError as exc:
	error, = exc.args
	print( sys.stderr, "Oracle code:", error.code)
	print( sys.stderr, "oracle message:", error.message)
