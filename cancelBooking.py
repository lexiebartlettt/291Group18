import cx_Oracle # the package used for accessing Oracle in Python

def cancelBooking(ticktNum, flightNum, depDate, curs):
  try:
    curs.connection.begin()
    
    queryStr = "SELECT price FROM flight_fares WHERE(flightno = 'flightNum' and fare = 'depDate')"
    queryStr = queryStr.replace("flightNum", flightNum)
    queryStr = queryStr.replace("depDate", depDate)
    curs.execute(queryStr)
    fetcher = curs.fetchall()
    refund = fetcher[0][0]
    
    queryStr = "SELECT paid_price FROM tickets WHERE tno = ticketNum"
    queryStr = queryStr.replace("ticketNum", ticketNum)
    curs.execute(queryStr)
    fetcher = curs.fetchall()
    newPrice = fetcher[0][0] - refund
    
    queryStr = "UPDATE tickets SET price_paid = 'newPrice' WHERE tno = ticketNum"
    queryStr = queryStr.replace("ticketNum", ticketNum)
    queryStr = queryStr.replace("newPrice", newPrice)
    curs.execute(queryStr)
    
    queryStr = "DELETE FROM bookings WHERE(tno = ticketNum and flightno = 'flightNum')"
    queryStr = queryStr.replace("ticketNum", ticketNum)
    queryStr = queryStr.replace("flightNum", flightNum)
    curs.execute(queryStr)
    
    curs.connection.commit()
    print("You have successfully cancelled your booking")
  
  except cx_Oracle.DatabaseError as exc:
    error, = exc.args
    curs.connection.rollback()
    print( "Your booking was not cancelled ")
    print( sys.stderr, "Oracle code:", error.code)
    print( sys.stderr, "Oracle message:", error.message)
