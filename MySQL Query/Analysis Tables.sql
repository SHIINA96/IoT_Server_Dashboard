use arduino;
create table Humidity_Analysis
(
	Data_ID int auto_increment not null  primary key,
    Humidity_Mean double(16,2),
    Humidity_Median double(16,2),
    Humidity_Mode double(16,2),
    Data_Time datetime null default current_timestamp
    );
    
use arduino;    
create table Temperature_Analysis
(
	Data_ID int auto_increment not null primary key,
    Temperature_Mean double(16,2),
    Temperature_Median double(16,2),
    Temperature_Mode double(16,2),
    Data_Time datetime null default current_timestamp
    );
    