select Humidity_Value,Data_Time 
from Humidity_Data 
where to_days(Data_Time) = to_days(now());