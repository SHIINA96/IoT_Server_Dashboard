insert into Humidity_Analysis (Humidity_Mode) 
select AVG(distinct Humidity_Value)
from(
select T1.Humidity_Value from Humidity_Data  T1,  Humidity_Data T2
group by T1.Humidity_Value
having sum(case when T2.Humidity_Value >= T1.Humidity_Value then 1 else 0 end) >= count(*)/2
and sum(case when T2.Humidity_Value <= T1.Humidity_Value then 1 else 0 end) >= count(*)/2
) tmp;