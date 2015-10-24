select  t.tno, t.name, to_char(b.dep_date, 'dd-mon-yy'), t.paid_price, b.flightno, b.dep_date
from tickets t, bookings b
where b.tno = t.tno
and t.email = :email
