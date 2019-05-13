use arduino;
delimiter //
create procedure Temperature_Analysis()
begin
insert into Temperature_Analysis (Temperature_Median) 
select Temperature_Value
from Temperature_Data
group by Temperature_Value
having count(*) >= (
select max(cnt) from (select count(*) cnt from Temperature_Data group by Temperature_Value) tmp
) ;

insert into Temperature_Analysis (Temperature_Mode) 
select AVG(distinct Temperature_Value)
from(
select T1.Temperature_Value from Temperature_Data  T1,  Temperature_Data T2
group by T1.Temperature_Value
having sum(case when T2.Temperature_Value >= T1.Temperature_Value then 1 else 0 end) >= count(*)/2
and sum(case when T2.Temperature_Value <= T1.Temperature_Value then 1 else 0 end) >= count(*)/2
)tmp;

insert into Temperature_Analysis (Temperature_Mean) 
select avg(Temperature_Value)
from Temperature_Data;
end//
delimiter ;