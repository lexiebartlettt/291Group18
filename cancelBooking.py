import cx_Oracle # the package used for accessing Oracle in Python

def cancelBooking(ticktNum, flightNum, fareType, curs):
  try:
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
  
  except cx_Oracle.DatabaseError as exc:
    error, = exc.args
    print( sys.stderr, "Oracle code:", error.code)
    print( sys.stderr, "Oracle message:", error.message)
