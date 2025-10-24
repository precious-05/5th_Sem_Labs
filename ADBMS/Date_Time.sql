-- ========================================
-- DATE       → Format: YYYY-MM-DD
-- DATETIME   → Format: YYYY-MM-DD HH:MI:SS
-- TIMESTAMP  → Format: YYYY-MM-DD HH:MI:SS
-- YEAR       → Format: YYYY or YY
-- TIME       → Format: hh:mm:ss

-- Commonly used functions:
-- CURDATE() → Returns current date
-- DATEDIFF(date1, date2) → Returns difference (in days)
-- TIMEDIFF(time1, time2) → Returns time difference

-- ========================================
-- PROBLEM 1: ORDERS TABLE IMPLEMENTATION
-- ========================================

CREATE DATABASE Practice;
USE Practice;


-- 1. Create the Orders table
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    price DECIMAL(10, 2),
    quantity INT,
    order_date DATE,
    delivery_date DATE
);


-- 2. Insert 8 rows into Orders table
INSERT INTO Orders VALUES (1, 'T-shirt', 25.99, 2, '2023-07-15', '2023-07-25');
INSERT INTO Orders VALUES (2, 'Jeans', 49.95, 1, '2023-07-17', '2023-07-20');
INSERT INTO Orders VALUES (3, 'Shoes', 69.50, 1, '2023-07-20', '2023-07-30');
INSERT INTO Orders VALUES (4, 'Sunglasses', 12.75, 3, '2023-07-22', '2023-07-28');
INSERT INTO Orders VALUES (5, 'Backpack', 34.99, 2, '2023-07-25', '2023-07-29');
INSERT INTO Orders VALUES (6, 'Headphones', 59.99, 1, '2023-07-29', '2023-08-05');
INSERT INTO Orders VALUES (7, 'Smartphone', 299.99, 2, '2023-07-29', '2023-11-01');
INSERT INTO Orders VALUES (8, 'Laptop', 799.95, 1, '2023-07-29', '2025-08-01');




-- ========================================
-- QUERIES & SOLUTIONS
-- ========================================

-- 3) Retrieve all orders placed on '2023-07-15'
SELECT * FROM Orders WHERE order_date='2023-07-15';

-- 4) Find number of days required to deliver 'Shoes'
SELECT product_name, DATEDIFF(delivery_date, order_date) AS delivery_time
FROM Orders WHERE product_name = 'Shoes';

-- 5) Find all orders received between '2023-07-15' and '2023-07-25'
SELECT * FROM Orders WHERE order_date BETWEEN '2023-07-15' AND '2023-07-25';


-- 6) Find all orders received today
SELECT * FROM Orders WHERE order_date = CURDATE();

-- 7) Calculate average delivery time (in days)
SELECT AVG(DATEDIFF(delivery_date, order_date)) AS avg_delivery_time FROM Orders;

-- ========================================
-- NOTE:
-- MySQL supports only 2 parameters in DATEDIFF(date1, date2)
-- Returns result in DAYS (date1 - date2)
-- ========================================

-- 8) Find the number of months required to deliver smartphone
-- (MySQL will only return days, not months)
SELECT product_name, DATEDIFF(delivery_date, order_date) AS delivery_days FROM Orders
WHERE product_name = 'Smartphone';

-- In MS SQL Server we could use:
-- SELECT DATEDIFF(month, order_date, delivery_date) AS delivery_months FROM Orders;

-- 9) Find products requiring more than 2 months to deliver
-- (MySQL version - estimate months using days/30)
SELECT product_name FROM Orders WHERE (DATEDIFF(delivery_date,order_date)/30) >2;

-- 10) Find products requiring more than 3 weeks to deliver
SELECT product_name FROM Orders WHERE (DATEDIFF(delivery_date,order_date)/7) >3;

-- 11) Find products requiring more than 1 year to deliver
SELECT product_name FROM Orders WHERE (DATEDIFF(delivery_date,order_date)/365) >1;




-- ========================================
-- PROBLEM 2: EMP_TIME TABLE
-- ========================================


-- i) Create Emp_time table
CREATE TABLE Emp_time (
    Eid VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(30),
    Start_time TIME,
    End_time TIME
);

-- ii) Insert records
INSERT INTO Emp_time VALUES ('E101', 'Hari', '10:15:00', '18:00:00');
INSERT INTO Emp_time VALUES ('E102', 'Malati', '08:00:00', '15:30:00');
INSERT INTO Emp_time VALUES ('E103', 'Kalyan', '09:30:00', '17:00:00');

-- iii) Select all employees and their total working hours
SELECT Eid, Name, TIMEDIFF(End_time,Start_time) AS Total_Working_Hours FROM Emp_time ;

-- iii) Select all employees and their total working hours
SELECT Eid, Name, TIMEDIFF(End_time, Start_time) AS Total_Working_Hours FROM Emp_time;

-- iv) Find employees with least working hours
SELECT Eid, Name, TIMEDIFF(End_time, Start_time) AS Work_Duration FROM Emp_time ORDER BY Work_Duration ASC;

-- v) Find employees with longest working hours
SELECT Eid, Name, TIMEDIFF(End_time, Start_time) AS Work_Duration FROM Emp_time 
ORDER BY Work_Duration DESC;

-- vi) Select employee who worked longest hours
SELECT Eid, Name, TIMEDIFF(End_time, Start_time) AS Work_Duration
FROM Emp_time ORDER BY Work_Duration DESC
LIMIT 1;

-- vii) Find employees who worked more than 7 hours
SELECT Name FROM Emp_time
WHERE TIMEDIFF(End_time, Start_time) > '07:00:00';

-- viii) Display employee(s) whose name starts with 'M' and worked more than 7 hours
SELECT Name FROM Emp_time WHERE Name LIKE 'M%' 
AND TIMEDIFF(End_time, Start_time) > '07:00:00';

-- ix) Delete all records (to insert new data later)
TRUNCATE TABLE Emp_time;  -- table will still exist

SELECT * FROM Emp_time;

DROP TABLE Emp_time;  -- Removes the table permanently
SELECT * FROM Emp_time;



















-- ========================================
-- DATE       → Format: YYYY-MM-DD
-- DATETIME   → Format: YYYY-MM-DD HH:MI:SS
-- TIMESTAMP  → Format: YYYY-MM-DD HH:MI:SS
-- YEAR       → Format: YYYY or YY
-- TIME       → Format: hh:mm:ss

-- Commonly used functions:
-- CURDATE() → Returns current date
-- DATEDIFF(date1, date2) → Returns difference (in days)
-- TIMEDIFF(time1, time2) → Returns time difference

-- ========================================
-- PROBLEM 1: ORDERS TABLE IMPLEMENTATION
-- ========================================

-- 1. Create the Orders table

-- 2. Insert 8 rows into Orders table

-- ========================================
-- QUERIES & SOLUTIONS
-- ========================================

-- 3) Retrieve all orders placed on '2023-07-15'

-- 4) Find number of days required to deliver 'Shoes'

-- 5) Find all orders received between '2023-07-15' and '2023-07-25'

-- 6) Find all orders received today

-- 7) Calculate average delivery time (in days)

-- ========================================
-- NOTE:
-- MySQL supports only 2 parameters in DATEDIFF(date1, date2)
-- Returns result in DAYS (date1 - date2)
-- ========================================

-- 8) Find the number of months required to deliver smartphone
-- (MySQL will only return days, not months)

-- In MS SQL Server we could use:
-- SELECT DATEDIFF(month, order_date, delivery_date) AS delivery_months FROM Orders;

-- 9) Find products requiring more than 2 months to deliver
-- (MySQL version - estimate months using days/30)

-- 10) Find products requiring more than 3 weeks to deliver

-- 11) Find products requiring more than 1 year to deliver

-- ========================================
-- PROBLEM 2: EMP_TIME TABLE
-- ========================================

-- i) Create Emp_time table

-- ii) Insert records

-- iii) Select all employees and their total working hours

-- iii) Select all employees and their total working hours

-- iv) Find employees with least working hours

-- v) Find employees with longest working hours

-- vi) Select employee who worked longest hours

-- vii) Find employees who worked more than 7 hours

-- viii) Display employee(s) whose name starts with 'M' and worked more than 7 hours

-- ix) Delete all records (to insert new data later)
-- table will still exist

-- Removes the table permanently
