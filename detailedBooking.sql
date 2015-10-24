select  t.tno, t.name, b.flightno, f.src, f.dst, b.seat, b.fare,  to_char(b.dep_date, 'dd-mon-yy') as Dep_date, t.paid_price
from tickets t, bookings b, flights f
where b.tno = t.tno
and f.flightno = b.flightno
and b.tno = :ticket
and b.flightno = :flight
and b.dep_date = to_date(:depdate, 'dd-mon-yy')
