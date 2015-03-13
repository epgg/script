drop table if exists yearlyMonthlyLength;
create table yearlyMonthlyLength (
year smallint unsigned not null,
month tinyint unsigned not null,
length tinyint unsigned not null
);
load data local infile 'ymd' into table yearlyMonthlyLength;
