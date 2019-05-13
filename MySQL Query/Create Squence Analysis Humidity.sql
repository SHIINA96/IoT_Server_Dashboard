use arduino;
delimiter //
create procedure Humidity_Analysis()
begin
insert into Humidity_Analysis (Humidity_Median) 
select Humidity_Value
from Humidity_Data
group by Humidity_Value
having count(*) >= (
select max(cnt) from (select count(*) cnt from Humidity_Data group by Humidity_Value) tmp
) ;

insert into Humidity_Analysis (Humidity_Mode) 
select AVG(distinct Humidity_Value)
from(
select T1.Humidity_Value from Humidity_Data  T1,  Humidity_Data T2
group by T1.Humidity_Value
having sum(case when T2.Humidity_Value >= T1.Humidity_Value then 1 else 0 end) >= count(*)/2
and sum(case when T2.Humidity_Value <= T1.Humidity_Value then 1 else 0 end) >= count(*)/2
)tmp;

insert into Humidity_Analysis (Humidity_Mean) 
select avg(Humidity_Value)
from Humidity_Data;
end//
delimiter ;