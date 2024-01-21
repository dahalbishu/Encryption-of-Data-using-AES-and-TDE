/*
use master;

--Create Master Key
CREATE MASTER KEY ENCRYPTION
BY PASSWORD='rajatd@n';


--Create Certificate protected by master key
CREATE CERTIFICATE TDE_Cert
WITH 
SUBJECT='Database_Encryption';

create database rajat;

use rajat;

create table user_info(
fullname varchar(50) NOT NULL,
email varchar(50) NOT NULL primary key,
ccn VARCHAR(256) NOT NULL
);

insert into user_info values('Rajat Dulal', 'rjtdulal@gmail.com', 1234);
insert into user_info values('Sirjana Bhatta', 'sirjana@gmail.com', 8976);

*/
use rajat;
select * from user_info;

--Create database encryption key
CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE TDE_Cert;


--Enable Encryption
ALTER DATABASE rajat
SET ENCRYPTION ON;

--Backup Certificate

use master;

BACKUP CERTIFICATE TDE_Cert
TO FILE = 'C:\Users\rjtdu\OneDrive\Desktop\Hitachi_techenergy\TDE_Cert'
WITH PRIVATE KEY (file='C:\Users\rjtdu\OneDrive\Desktop\Hitachi_techenergy\TDE_CertKey.pvk',
ENCRYPTION BY PASSWORD='rajatd@n') 

select name, is_encrypted from sys.databases;
select * from sys.certificates;

DELETE from user_info where fullname = 'Bisheram';

delete table user_info;