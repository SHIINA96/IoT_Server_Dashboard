insert into Humidity_Analysis (Humidity_Mean) 
select avg(Humidity_Value)
from Humidity_Data