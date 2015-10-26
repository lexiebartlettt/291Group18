def cancelBooking(ticktNum, flightNum, fareType):
  try:
    # Establish a connection in Python
		connection = cx_Oracle.connect(conString)
		# create a cursor 
		curs = connection.cursor()
		#get name
		passengerName = input("Your name [%s]: " % getpass.getuser())
		if not passengerName:
			passengerName=getpass.getuser()
    
    queryStr = "SELECT price FROM flight_fares WHERE(flightno = 'flightNum' and fare = 'fareType')"
    queryStr = queryStr.replace("flightNum", flightNum)
    queryStr = queryStr.replace("fareType", fareType)
    curs.execute(queryStr)
    refund = curs.fetch()
    
    queryStr = "SELECT paid_price FROM tickets WHERE tno = 'ticketNum'"
    queryStr = queryStr.replace("ticketNum", ticketNum)
    curs.execute(queryStr)
    newPrice = curs.fetch() - refund
    
    queryStr = "UPDATE tickets SET price_paid = 'newPrice' WHERE tno = 'ticketNum'"
    queryStr = queryStr.replace("ticketNum", ticketNum)
    queryStr = queryStr.replace("newPrice", newPrice)
    curs.execute(queryStr)
    
    queryStr = "DELETE FROM bookings WHERE(tno = 'ticketNum' and flightno = 'flightNum')
    queryStr = queryStr.replace("ticketNum", ticketNum)
    queryStr = queryStr.replace("flightNum", flightNum)
    curs.execute(queryStr)
    
    # close the connection
		curs.close()
		connection.close()

	except cx_Oracle.DatabaseError as exc:
		error, = exc.args
		print( sys.stderr, "Oracle code:", error.code)
		print( sys.stderr, "Oracle message:", error.message)
