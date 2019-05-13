select Humidity_Value,Data_Time
from Humidity_Data where to_days(NOW()) - TO_DAYS(Data_Time) <= 1;