-- =======================
--        Problem 1
-- =======================

-- 1) Create any database name  
CREATE DATABASE OrgDB;
USE OrgDB;

-- 2) Create two tables Employee and Department with following columns 
--    using appropriate data types and insert the following data.  
--    Your table must be in following form:  
CREATE TABLE Department (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50),
    hod_name VARCHAR(50)
);

CREATE TABLE Employee (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    position VARCHAR(50),
    salary INT,
    dept_id INT,
     FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
);

-- INSERT DATA

INSERT INTO Department (dept_id, dept_name, hod_name) VALUES
(1, 'Sales', 'Janak'),
(2, 'Marketing', 'Madhav'),
(3, 'Finance', 'Sapana'),
(4, 'Operations', 'Durga');

INSERT INTO Employee (emp_id, emp_name, position, salary, dept_id) VALUES
(1, 'Anish', 'Manager', 50000, 3),
(2, 'Sita', 'Secretary', 25000, 1),
(3, 'Ronit', 'Analyst', 25000, 2),
(4, 'Riya', 'Manager', 40000, 4);


-- 3) Perform the following Join Operations   
--    a) Inner Join  
SELECT emp_name, position, salary, dept_name
FROM Employee
INNER JOIN Department
ON Employee.dept_id = Department.dept_id;


--    b) Left Outer Join  
SELECT emp_name, position, salary, dept_name
FROM Employee
LEFT JOIN Department
ON Employee.dept_id = Department.dept_id;

--    c) Right Outer Join  
SELECT emp_name, position, salary, dept_name
FROM Employee
RIGHT JOIN Department
ON Employee.dept_id = Department.dept_id;

--    d) Full Join  
SELECT emp_name, position, salary, dept_name
FROM Employee
LEFT JOIN Department
ON Employee.dept_id = Department.dept_id
UNION
SELECT emp_name, position, salary, dept_name
FROM Employee
RIGHT JOIN Department
ON Employee.dept_id = Department.dept_id;

--    e) Natural Join  
SELECT emp_id, emp_name, dept_id, dept_name
FROM Employee
NATURAL JOIN Department;

--    f) Cross Join
SELECT emp_name, dept_name
FROM Employee
CROSS JOIN Department;  



-- 4) Write SQL queries to:  
--    i) Find Employee names with their department  
SELECT emp_name,dept_name
FROM Employee
LEFT JOIN Department 
ON Employee.dept_id = Department.dept_id;


--    ii) Find emp_name, position, salary of employee who works in Finance department  
SELECT emp_name,position,salary
FROM Employee
LEFT JOIN Department
ON Employee.dept_id = Department.dept_id
WHERE dept_name='finance';



--    iii) Find emp_name of employee who works in Sales department  
SELECT emp_name
FROM Employee
INNER JOIN Department
ON Employee.dept_id = Department.dept_id
WHERE dept_name = 'Sales';

--    iv) Find the information of employee who works in Marketing department 
SELECT *
FROM Employee
INNER JOIN Department
ON Employee.dept_id = Department.dept_id
WHERE dept_name = 'Marketing';


 
--    v) Find the HOD of Riya  
SELECT D.hod_name
FROM Employee E
JOIN Department D
ON E.dept_id = D.dept_id
WHERE E.emp_name = 'Riya';


-- =======================
--  Problem 2
-- =======================

-- 1) Create two tables emp_civildepartment and emp_computerdepartment  
--    with following columns (emp_id, emp_name, address) and insert data.  

 CREATE TABLE emp_civildepartment (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    address VARCHAR(50)
);

CREATE TABLE emp_computerdepartment (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    address VARCHAR(50)
);

-- Step 2: Insert Data
INSERT INTO emp_civildepartment VALUES
(1, 'Kapil', 'Chitwan'),
(2, 'Ujwal', 'Dharan'),
(3, 'Pradip', 'Palpa'),
(4, 'Prakash', 'Kathmandu'),
(5, 'Supriya', 'Mahendranagar');

INSERT INTO emp_computerdepartment VALUES
(1, 'Mukunda', 'Surkhet'),
(2, 'Santosh', 'Pokhara'),
(3, 'Pradip', 'Palpa'),
(4, 'Jasbin', 'Kathmandu'),
(5, 'Supriya', 'Mahendranagar');


-- 2) Perform the following Set Operations:  
--    a) UNION  
-- Combines results from both tables but removes duplicates
SELECT emp_name FROM emp_civildepartment
UNION
SELECT emp_name FROM emp_computerdepartment;


--    b) UNION ALL  
-- Same as UNION but keeps duplicates
SELECT emp_name FROM emp_civildepartment
UNION ALL
SELECT emp_name FROM emp_computerdepartment;

--    c) INTERSECT  
-- Returns only common values who are in both tables
SELECT c.emp_name
FROM emp_civildepartment c
INNER JOIN emp_computerdepartment d
ON c.emp_name = d.emp_name;




--    d) EXCEPT  

SELECT d.emp_name
FROM emp_computerdepartment d
LEFT JOIN emp_civildepartment c
ON d.emp_name = c.emp_name
WHERE c.emp_name IS NULL;


-- 3) Write SQL queries to:  
--    i) Find the name of employee who works either in Civil or Computer department  (UNION)
SELECT emp_name FROM emp_civildepartment
UNION
SELECT emp_name FROM emp_computerdepartment;

--    ii) Find the name of employee who works in both Civil and Computer department  (INTERSECT)
SELECT c.emp_name
FROM emp_civildepartment c
INNER JOIN emp_computerdepartment d
ON c.emp_name = d.emp_name;

--    iii) Find the name of employee who works in Computer department but not in Civil department   (EXCEPT)
SELECT d.emp_name
FROM emp_computerdepartment d
LEFT JOIN emp_civildepartment c
ON d.emp_name = c.emp_name
WHERE c.emp_name IS NULL;

--    iv) Find the common address where both Computer and Civil department employees live   (INTERSECT)
SELECT c.address
FROM emp_civildepartment c
INNER JOIN emp_computerdepartment d
ON c.address = d.address;

