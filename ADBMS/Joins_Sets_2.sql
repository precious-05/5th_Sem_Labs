USE OrgDB;
-- LEFT JOIN (Agar match nahi milta, to right table ke columns me NULL show hota hai)
-- 4) Write SQL queries to:  
--    i) Find Employee names with their department  
SELECT e.emp_name , d.dept_name
FROM employee e INNER JOIN department d ON e.dept_id=d.dept_id;


--    ii) Find emp_name, position, salary of employee who works in Finance department  
SELECT e.emp_name, e.position, e.salary, d.dept_name
FROM employee e
LEFT JOIN department d 
ON e.dept_id=d.dept_id
WHERE dept_name='finance';


--    iii) Find emp_name of employee who works in Sales department  
SELECT e.emp_name, d.dept_name
FROM employee e
LEFT JOIN department d 
ON e.dept_id=d.dept_id
WHERE dept_name='sales';      -- After join applies further filtering

--    iv) Find the information of employee who works in Marketing department 
SELECT e.emp_name, d.dept_name
FROM employee e
LEFT JOIN department d 
ON e.dept_id=d.dept_id
WHERE dept_name='marketing';

 
--    v) Find the HOD of Riya  
SELECT e.emp_name, d.hod_name
FROM employee e
LEFT JOIN department d 
ON e.dept_id=d.dept_id
WHERE emp_name='riya';



-- =======================
--  Problem 2
-- =======================

-- 3) Write SQL queries to:  
--    i) Find the name of employee who works either in Civil or Computer department  
SELECT * FROM emp_civildepartment
UNION
SELECT * FROM emp_computerdepartment;



--    ii) Find the name of employee who works in both Civil and Computer department
SELECT c.emp_name       -- Because INTERSECT does'nt directly work in MYSQL
FROM emp_civildepartment c
INNER JOIN emp_computerdepartment d
ON c.emp_name = d.emp_name;


--    iii) Find the name of employee who works in Computer department but not in Civil department   
SELECT c.emp_name       -- Because EXCEPT does'nt directly work in MYSQL
FROM emp_civildepartment c
LEFT JOIN emp_computerdepartment d
ON c.emp_name = d.emp_name
WHERE c.emp_name IS NULL;   -- No — LEFT JOIN alone doesn't behave exactly like EXCEPT unless you also add WHERE right_table.column IS NULL

--    iv) Find the common address where both Computer and Civil department employees live  
SELECT c.address
FROM emp_civildepartment c
INNER JOIN emp_computerdepartment d
ON c.address = d.address;
