create event Analysis_Temperature_Hourly
on schedule every 1 hour
on completion preserve enable
do call Temperature_Analysis();