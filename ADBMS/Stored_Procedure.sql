CREATE DATABASE Institute;
USE Institute;


CREATE TABLE Employee(
 emp_id INT PRIMARY KEY,
 emp_name VARCHAR(30),
 position VARCHAR(300),
 salary INT,
 dept_id INT
);


CREATE TABLE Department(
 dept_id INT PRIMARY KEY ,               -- ADDING CONSTRAINT
 dept_name VARCHAR(30) NOT NULL,
 location VARCHAR(30) NOT NULL,
 budget INT 
);  


ALTER TABLE Employee 
ADD CONSTRAINT foreign_key FOREIGN KEY(dept_id) REFERENCES Department(dept_id);


-- 4. Insert Records into Department Table
INSERT INTO Department VALUES (1, 'HR', 'Lahore', 600000);
INSERT INTO Department VALUES (2, 'Finance', 'Karachi', 850000);
INSERT INTO Department VALUES (3, 'IT', 'Islamabad', 1200000);
INSERT INTO Department VALUES (4, 'Marketing', 'Lahore', 700000);
INSERT INTO Department VALUES (5, 'Admin', 'Multan', 500000);


-- 5. Insert Records into Employee Table
INSERT INTO Employee VALUES (101, 'Ali Khan', 'HR Manager', 90000, 1);
INSERT INTO Employee VALUES (102, 'Sara Ahmed', 'Accountant', 80000, 2);
INSERT INTO Employee VALUES (103, 'Usman Tariq', 'Software Engineer', 120000, 3);
INSERT INTO Employee VALUES (104, 'Hina Malik', 'Marketing Executive', 75000, 4);
INSERT INTO Employee VALUES (105, 'Bilal Hassan', 'Office Assistant', 50000, 5);


-- Creating Stored Procedure without parameters
/*DELIMITER //  
CREATE PROCEDURE getallEmployee ()  
BEGIN  
SELECT * FROM employee;  
END //  
DELIMITER ; */


DELIMITER //
CREATE PROCEDURE l_join()
BEGIN
SELECT e.emp_id, e.emp_name, e.position FROM Employee E 
RIGHT JOIN Department D ON e.dept_id=d.dept_id WHERE e.emp_name REGEXP '^[a-d]';
END //
DELIMITER ;
-- DROP PROCEDURE l_join;
CALL l_join;


DELIMITER //
CREATE PROCEDURE fetch_all_emp()
BEGIN
SELECT * FROM Employee;
END //
DELIMITER ;

CALL fetch_all_emp();
DROP PROCEDURE fetch_all_emp;


-- Queries Using Parameters
DELIMITER //
CREATE PROCEDURE emp_proc(dept VARCHAR(30), salary INT)
BEGIN
SELECT emp_name,salary FROM Employee WHERE position=dept OR salary>salary;
END //
DELIMITER ;


CALL emp_proc('Accountant', 1000);






-- Creating Views
/*CREATE VIEW view_name AS  
SELECT column1, column2, ...  
FROM table_name  
WHERE condition;  */


-- 1). Create view for display the emp_id ,emp_name, position  of employee  

CREATE VIEW admin AS 
SELECT  emp_id ,emp_name, position FROM Employee 
WHERE salary>20000;

-- 2) Create view for display emp_id, emp_name, position, dept_name, location  
CREATE VIEW user AS 
SELECT e.emp_id, e.emp_name, e.position, d.dept_name, d.location
FROM Employee e
JOIN Department d ON e.dept_id=d.dept_id 
WHERE salary>20000;




-- DROP DATABASE Institute;
