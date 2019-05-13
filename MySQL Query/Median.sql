insert into Humidity_Analysis (Humidity_Median) select Humidity_Value
from Humidity_Data
group by Humidity_Value
having count(*) >= (
select max(cnt) from (select count(*) cnt from Humidity_Data group by Humidity_Value) tmp
) 