import cx_Oracle # the package used for accessing Oracle in Python

def cancelBooking(ticketNum, flightNum, depDate, fareType, curs):
  try:
    # begin transaction
    curs.connection.begin()
    
    # get the cost of the booking being canceled
    queryStr = "SELECT price FROM flight_fares WHERE(flightno = 'flightNum' and fare = 'fareType')"
    queryStr = queryStr.replace("flightNum", flightNum)
    queryStr = queryStr.replace("fareType", fareType)
    curs.execute(queryStr)
    fetcher = curs.fetchall()
    refund = fetcher[0][0]
    
    # get the total amount paid for this ticket
    queryStr = "SELECT paid_price FROM tickets WHERE tno = ticketNum"
    queryStr = queryStr.replace("ticketNum", str(ticketNum))
    curs.execute(queryStr)
    fetcher = curs.fetchall()
    newPrice = fetcher[0][0] - refund
    
    # adjust the ticket price to refund the amount paid for the booking being canceled
    queryStr = "UPDATE tickets SET paid_price = newPrice WHERE tno = ticketNum"
    queryStr = queryStr.replace("ticketNum", str(ticketNum))
    queryStr = queryStr.replace("newPrice", str(newPrice))
    curs.execute(queryStr)
    
    # delete the booking to be canceled
    queryStr = "DELETE FROM bookings WHERE(tno = ticketNum and flightno = 'flightNum' and dep_date = to_date('depDate', 'dd-mon-yy'))"
    queryStr = queryStr.replace("ticketNum", str(ticketNum))
    queryStr = queryStr.replace("flightNum", flightNum)
    queryStr = queryStr.replace("depDate", depDate)
    curs.execute(queryStr)
    
    # end transaction and display confirmation
    curs.connection.commit()
    print("You have successfully cancelled your booking")
    input("Press 'Enter' to return to main menu")
  # catch database error
  except cx_Oracle.DatabaseError as exc:
    # rollback all changes and display descriptive message
    curs.connection.rollback()
    print( "Your booking was not successfully cancelled")
    input("Press 'Enter' to return to main menu")
