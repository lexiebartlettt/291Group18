Create view allFlights as
SELECT flightno1, flightno2, layover, price, src, dst, dep_date
	FROM  (( SELECT flightno as flightno1, NULL as flightno2, NULL as layover, dep_date, dst, src, price
		FROM available_flights
	 	)
		UNION
              ( SELECT flightno1, flightno2, layover, dep_date, dst, src, price
		FROM good_connections
		)
		)



