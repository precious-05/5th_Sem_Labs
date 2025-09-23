CREATE DATABASE CompanyDB;
USE CompanyDB;

-- Employees table
CREATE TABLE Employees(
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    dept_id INT,
    salary INT
);

-- Departments table
CREATE TABLE Departments(
	 dept_id INT PRIMARY KEY,
     dept_name VARCHAR(50)
);

-- Projects table
CREATE TABLE Projects (
    proj_id INT PRIMARY KEY,
    proj_name VARCHAR(50),
    dept_id INT
);


-- EmployeeProjects table (which employees are assigned to projects)
CREATE TABLE EmployeeProjects (
    emp_id INT,
    proj_id INT,
    role VARCHAR(50),
    PRIMARY KEY (emp_id, proj_id)
);



-- Insert Departments
INSERT INTO Departments VALUES
(1, 'HR'),
(2, 'IT'),
(3, 'Finance');

-- Insert Employees
INSERT INTO Employees VALUES
(101, 'Alice', 1, 5000),
(102, 'Bob', 2, 6000),
(103, 'Charlie', 2, 7000),
(104, 'David', 3, 5500),
(105, 'Eve', NULL, 4500);

-- Insert Projects
INSERT INTO Projects VALUES
(201, 'Recruitment System', 1),
(202, 'Website Upgrade', 2),
(203, 'Audit Tool', 3);

-- Insert EmployeeProjects
INSERT INTO EmployeeProjects VALUES
(101, 201, 'Manager'),
(102, 202, 'Developer'),
(103, 202, 'Tester'),
(104, 203, 'Auditor');



-- 1.Show each employee's name along with their department name
SELECT employees.name, departments.dept_name
FROM employees 
LEFT JOIN departments
ON employees.dept_id=departments.dept_id;

-- 2. Show all departments and the employees who work in them (include departments even if they don't have any employees)
SELECT d.dept_name, e.name
FROM employees e
RIGHT JOIN departments d
ON e.dept_id = d.dept_id;

-- 3. Show all projects and the employees assigned to them.
SELECT  p.proj_name,e.name
FROM  projects p
LEFT JOIN employees e
ON p.dept_id=e.dept_id;

-- 4. Show all employees and the projects they are working on (if no project is assigned, still show the employee).
SELECT e.name,p.proj_name
FROM employees e
LEFT JOIN projects p
ON e.dept_id=p.dept_id;


-- 5. Show all departments with the projects under them (include departments even if they don’t have any projects).
SELECT d.dept_name, p.proj_name
FROM departments d
LEFT JOIN projects p
ON d.dept_id=p.dept_id;


