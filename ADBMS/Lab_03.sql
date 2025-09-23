-- Create any database and in such database create a table named employee  
-- with the following columns  by considering employee_id as primary key 
-- employee(empoyee_id,first_name,last_name,age,address, department,postion,salary)  
-- create table employee(employee_id int PRIMARY KEY,first_name varchar(20),last_name 
-- varchar(20),age int,address varchar(30),department varchar(30), position varchar(30),salary  decimal(10,2));  

CREATE DATABASE Company;
USE Company;
CREATE TABLE Employees(
	employee_id INT PRIMARY KEY,
    first_name  VARCHAR(20),
    last_name VARCHAR(20),
    age INT,
    address VARCHAR(30),
    department VARCHAR(30),
    position VARCHAR(30),
    salary decimal(10,2)
);

INSERT INTO Employees VALUES(1,'anish','sharma',26,'kathmandu','finance','manager',80000.25); 
INSERT INTO Employees VALUES(2,'roshan','pokhrel',28,'pokhara','sales','analyst',60000.45); 
INSERT INTO Employees VALUES(3,'aakriti','bagale',30,'butwal','purchase','manager',95000.52); 
INSERT INTO Employees VALUES(4,'rojina','karki',25,'pokhara','marketing','manager',85000.55); 
INSERT INTO Employees VALUES(5,'keshav','ghimire',35,'kathmandu','purchase','analyst',65000.35); 
INSERT INTO Employees VALUES(6,'roshan','pandey',38,'chitwan','operations','analyst',70000.12); 
INSERT INTO Employees VALUES(7,'sita','pokhrel',23,'lalitpur','marketing','analyst',68000.85); 
INSERT INTO Employees VALUES(8,'srijana','bhattrai',29,'butwal','finance','analyst',62000.65); 
INSERT INTO Employees VALUES(9,'niraj','acharya',40,'kathmandu','sales','manager',90000.54); 
INSERT INTO Employees VALUES(10,'nikita','giri',15,'pokhara','purchase','secretary',25000.86); 


-- Arithmetic, logical and relational operators  
-- 1. Display the first_name and last_name of employee whose deparment is finance 

SELECT first_name, last_name FROM Employees
WHERE department = 'finance';

--  2. Display all the information of employee in employee table  whose address is not kathmandu  
SELECT * FROM Employees 
WHERE address!='kathmandu'; 

-- 3. Increment the salary of all employees by 15%  
UPDATE Employees 
SET salary=salary*1.15;

-- 4. Decrease  the salary of manager by 5%  
UPDATE Employees 
SET salary=salary*0.95
WHERE position='manager';  


-- 5. Delete information of employee whose age is less than 18
DELETE FROM Employees
WHERE age<18;

-- 6. Display the position of employee whose salary is greater than or equals to 50000 
SELECT DISTINCT position FROM Employees
WHERE salary >=50000; 
-- 7. Display information of employee whose position is manager and address is kathmandu  
SELECT * FROM Employees
WHERE position='manager' AND address='kathmandu';  

-- 9. Display information of employee who either live in pokhara or kathmandu but age is greater than 25  
SELECT * FROM Employees
WHERE (address='kathmandu' or address='pokhara') AND age>25;

-- 10. Display first_name,last_name and position of employee whose salary is in the range of 70000 to 80000  
SELECT first_name,last_name,position FROM Employees
WHERE salary BETWEEN 70000 AND 80000;

-- 11. Display first_name,last_name and position of employee whose salary is not in  the range of 70000 to 80000  
SELECT first_name,last_name,position FROM Employees
WHERE salary NOT BETWEEN 70000 AND 80000;

-- 12. Display the information of employee whose salary is equal to 69000,30000,35000,40000,71300,80500  
SELECT * FROM Employees
WHERE salary in (69000,30000,35000,40000,71300,80500);


-- 13. Display information of employee whose department is (sales, purchase ) but not salary equal to (69000,71300,80500)  
SELECT * FROM Employees
WHERE department IN('sales','purchase') AND salary NOT IN(69000,71300,80500);

-- Like operator with wildcard characters  
-- 14. Display information of employees whose first_name starts with letter ‘a’  
SELECT * FROM Employees
WHERE first_name LIKE 'a%';

-- 15. Display information of employees whose first_name starts with letter ‘ro’  
SELECT * FROM Employees
WHERE first_name LIKE 'ro%';

-- 16. Display information of employees whose last_name ends with letter ‘el’  
SELECT * FROM Employees
WHERE last_name LIKE '%el';



-- 17. Display information of employees whose first_name has exactly six characters  
SELECT * FROM Employees
WHERE first_name LIKE '______';

-- 18. Display information of employees whose first_name starts with r and has exactly six characters  
SELECT * FROM Employees
WHERE first_name LIKE 'r_____';

/*  
 
24. Display information of employees whose first_name begins with [a-s] and ends with l  
select * from employee where first_name like'[a-s]%l';  
25. Display information of employees whose first_name  does not start with d but ends with h  
select * from employee where first_name like '[^d]%h' ; 
*/

-- 19. Display the information of employees which contains substring  of first_name as  ‘sha’ 
SELECT * FROM Employees
WHERE first_name LIKE '%sha%';

-- 20. Display information of employees whose  second position of first_name contains letter ‘o’ 
SELECT * FROM Employees
WHERE first_name LIKE '_o%';

-- 21. Display the information of employees whose third postion of first_name contains the letter ‘s’
SELECT * FROM Employees
WHERE first_name LIKE '__s%';

-- 22. Display information of employees which have first_name of at least six  characters  
SELECT * FROM Employees
WHERE first_name LIKE '______%';

-- 23. Display the information of employees whose first_name begins with a,k,m,s,r 
SELECT * FROM Employees
WHERE first_name LIKE '[akmsr]%';

