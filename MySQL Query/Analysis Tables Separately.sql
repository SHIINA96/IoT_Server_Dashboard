use arduino;
create table Humidity_Analysis_Mean
(  Data_ID int auto_increment not null  primary key,
    Humidity_Mean double(16,2),
    Data_Time datetime null default current_timestamp
);
create table Humidity_Analysis_Median
(  Data_ID int auto_increment not null  primary key,
    Humidity_Median double(16,2),
    Data_Time datetime null default current_timestamp
);
create table Humidity_Analysis_Mode
(  Data_ID int auto_increment not null  primary key,
    Humidity_Mode double(16,2),
    Data_Time datetime null default current_timestamp
);
create table Temperature_Analysis_Mean
(
	Data_ID int auto_increment not null primary key,
    Temperature_Mean double(16,2),
    Data_Time datetime null default current_timestamp
);
create table Temperature_Analysis_Median
(
	Data_ID int auto_increment not null primary key,
    Temperature_Median double(16,2),
    Data_Time datetime null default current_timestamp
);
create table Temperature_Analysis_Mode
(
	Data_ID int auto_increment not null primary key,
    Temperature_Mode double(16,2),
    Data_Time datetime null default current_timestamp
);
