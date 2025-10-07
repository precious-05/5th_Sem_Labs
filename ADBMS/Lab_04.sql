create database customer_db;  
USE customer_db;

-- 1) create a database named customers_db 
CREATE TABLE customers(
customer_id int,
name varchar(30) NOT NULL,
email varchar(255),
age int,
address varchar(30),
PRIMARY KEY(customer_id)); 

-- We have already added two constraints (PRIMARY KEY and NULL) while creating  table  customers. We can add constraints after creating table as well
-- Email must be unique of each customer 
ALTER TABLE customers
ADD UNIQUE(email); 

ALTER TABLE  customers ADD CONSTRAINT age_check CHECK(age>18);
ALTER TABLE customers ADD CHECK(age>18);

ALTER TABLE customers 
ALTER address SET DEFAULT 'bakhtpur';

-- 4) Now insert records of customer with and without violating constraints.  PRIMARY KEY 



























