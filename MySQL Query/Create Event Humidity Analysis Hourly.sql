create event Analysis_Humidity_Hourly
on schedule every 1 hour
on completion preserve enable
do call Humidity_Analysis();