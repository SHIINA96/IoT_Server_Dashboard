SELECT Humidity_Value,Data_Time
FROM Humidity_Data WHERE PERIOD_DIFF( date_format( now( ) , '%Y%m' ) , date_format( Data_time, '%Y%m' ) ) =1; 