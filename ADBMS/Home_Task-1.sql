-- ========================================
-- LAB 5 (DBMS) - Join and Set Operations
-- University of Layyah
-- ========================================

-- ========================================
-- PROBLEM 1
-- ========================================

-- Step 1: Create Database
CREATE DATABASE OrgDB;
USE OrgDB;

-- Step 2: Create Tables
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

-- Step 2: Insert Data
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


-- ========================================
-- JOIN OPERATIONS
-- ========================================

-- 1. Inner Join
SELECT emp_name, position, salary, dept_name
FROM Employee
INNER JOIN Department
ON Employee.dept_id = Department.dept_id;

-- 2. Left Outer Join
SELECT emp_name, position, salary, dept_name
FROM Employee
LEFT JOIN Department
ON Employee.dept_id = Department.dept_id;

-- 3. Right Outer Join
SELECT emp_name, position, salary, dept_name
FROM Employee
RIGHT JOIN Department
ON Employee.dept_id = Department.dept_id;

-- 4. Full Outer Join (using UNION)
SELECT emp_name, position, salary, dept_name
FROM Employee
LEFT JOIN Department
ON Employee.dept_id = Department.dept_id
UNION
SELECT emp_name, position, salary, dept_name
FROM Employee
RIGHT JOIN Department
ON Employee.dept_id = Department.dept_id;

-- 5. Natural Join
SELECT emp_id, emp_name, dept_id, dept_name
FROM Employee
NATURAL JOIN Department;

-- 6. Cross Join
SELECT emp_name, dept_name
FROM Employee
CROSS JOIN Department;

-- ========================================
-- REQUIRED QUERIES
-- ========================================

-- Employee names with their department
SELECT emp_name, dept_name
FROM Employee
INNER JOIN Department
ON Employee.dept_id = Department.dept_id;

-- emp_name, position, salary of employee in Finance
SELECT emp_name, position, salary
FROM Employee
INNER JOIN Department
ON Employee.dept_id = Department.dept_id
WHERE dept_name = 'Finance';

-- emp_name of employee in Sales
SELECT emp_name
FROM Employee
INNER JOIN Department
ON Employee.dept_id = Department.dept_id
WHERE dept_name = 'Sales';

-- Employee info who works in Marketing
SELECT *
FROM Employee
INNER JOIN Department
ON Employee.dept_id = Department.dept_id
WHERE dept_name = 'Marketing';

-- Find the HOD of Riya
SELECT D.hod_name
FROM Employee E
JOIN Department D
ON E.dept_id = D.dept_id
WHERE E.emp_name = 'Riya';

-- ========================================
-- PROBLEM 2
-- ========================================

-- Step 1: Create Tables
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

-- ========================================
-- SET OPERATIONS
-- ========================================

-- UNION
SELECT emp_name FROM emp_civildepartment
UNION
SELECT emp_name FROM emp_computerdepartment;

-- UNION ALL
SELECT emp_name FROM emp_civildepartment
UNION ALL
SELECT emp_name FROM emp_computerdepartment;

-- INTERSECT (using INNER JOIN)
SELECT c.emp_name
FROM emp_civildepartment c
INNER JOIN emp_computerdepartment d
ON c.emp_name = d.emp_name;

-- EXCEPT (using LEFT JOIN and NULL check)
SELECT d.emp_name
FROM emp_computerdepartment d
LEFT JOIN emp_civildepartment c
ON d.emp_name = c.emp_name
WHERE c.emp_name IS NULL;

-- ========================================
-- REQUIRED QUERIES
-- ========================================

-- Employees who work either in Civil or Computer
SELECT emp_name FROM emp_civildepartment
UNION
SELECT emp_name FROM emp_computerdepartment;

-- Employees who work in both Civil and Computer
SELECT c.emp_name
FROM emp_civildepartment c
INNER JOIN emp_computerdepartment d
ON c.emp_name = d.emp_name;

-- Employees in Computer but not in Civil
SELECT d.emp_name
FROM emp_computerdepartment d
LEFT JOIN emp_civildepartment c
ON d.emp_name = c.emp_name
WHERE c.emp_name IS NULL;

-- Common address between Civil and Computer
SELECT c.address
FROM emp_civildepartment c
INNER JOIN emp_computerdepartment d
ON c.address = d.address;



DROP DATABASE OrgDB;

/*What is Cartesian Product?

Cartesian product ka matlab hai → first table ke har row ko second table ke har row ke sath pair karna

Agar Table A me 3 rows hain aur Table B me 3 rows, to result hoga 3 × 3 = 9 rows

Agar ek table me 100 rows aur dusre me 50 rows, to result hoga 100 × 50 = 5000 rows

Where is CROSS JOIN used? (Real Scenarios)

Timetable Generation

Students × Days of Week → har student ke liye har din ek row ban jaayegi

Example: agar 5 students aur 7 din hain → 35 rows

E-commerce (Product Variations)

Suppose tumhare paas Products table hai aur Colors table

CROSS JOIN karega → har product ke saath har color ka combination

Example: 3 T-shirts × 4 colors = 12 variations

Testing / Dummy Data Generation

Random pairs banane ke liye CROSS JOIN use hota hai*/


