select  t.tno, t.name, to_char(b.dep_date, 'dd-mon-yy'), t.paid_price
from tickets t, bookings b
where b.tno = t.tno
and t.email = :email
