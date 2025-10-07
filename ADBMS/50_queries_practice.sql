-- Create any database and in such database create a table named employee  
-- with the following columns by considering employee_id as primary key 
-- employee(employee_id,first_name,last_name,age,address,department,position,salary)  
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



-- Insert at least 10 records into the Employees table  
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
-- 1. Display the first_name and last_name of employee whose department is finance  
SELECT first_name , last_name FROM Employees WHERE 	department='finance';


-- 2. Display all the information of employee in employee table whose address is not kathmandu  
SELECT * FROM Employees WHERE address!='kathmandu  ';


-- 3. Increment the salary of all employees by 15%  
UPDATE Employees SET salary=salary*0.15;


-- 4. Decrease the salary of manager by 5%  
UPDATE Employees SET salary=salary-0.95 WHERE position='manager'; 


-- 5. Delete information of employee whose age is less than 18  
DELETE FROM Employees WHERE age<18;


-- 6. Display the position of employee whose salary is greater than or equals to 50000  
SELECT DISTINCT position FROM Employees WHERE salary >=50000; 


-- 7. Display information of employee whose position is manager and address is kathmandu  
SELECT * FROM Employees WHERE position='manager' AND address='kathmandu';


-- 9. Display information of employee who either live in pokhara or kathmandu but age is greater than 25  
SELECT * FROM Employees
WHERE (address='kathmandu' or address='pokhara') AND age>25;   -- It shows same results even without brackets


-- 10. Display first_name,last_name and position of employee whose salary is in the range of 70000 to 80000  
SELECT first_name,last_name,position FROM Employees WHERE salary BETWEEN 70000 AND 80000;


-- 11. Display first_name,last_name and position of employee whose salary is not in the range of 70000 to 80000  
SELECT first_name,last_name,position FROM Employees WHERE salary NOT BETWEEN 70000 AND 80000;


-- 12. Display the information of employee whose salary is equal to 69000,30000,35000,40000,71300,80500  
SELECT * FROM Employees WHERE salary IN (69000,30000,35000,40000,71300,80500);


-- 13. Display information of employee whose department is (sales, purchase) but not salary equal to (69000,71300,80500)  
SELECT * FROM Employees WHERE department IN('sales','purchase') AND salary NOT IN(69000,71300,80500);




-- ====================== Like operator with wildcard characters ==================  
-- 14. Display information of employees whose first_name starts with letter ‘a’  
SELECT * FROM Employees WHERE first_name LIKE 'a%';

-- 15. Display information of employees whose first_name starts with letter ‘ro’  
SELECT * FROM Employees WHERE first_name LIKE 'ro%';


-- 16. Display information of employees whose last_name ends with letter ‘el’  
SELECT * FROM Employees WHERE last_name LIKE '%el';



-- 17. Display information of employees whose first_name has exactly six characters  
SELECT * FROM Employees WHERE first_name LIKE '______';


-- 18. Display information of employees whose first_name starts with r and has exactly six characters  
SELECT * FROM Employees WHERE first_name LIKE 'r_____';


-- 19. Display the information of employees which contains substring of first_name as ‘sha’  
SELECT * FROM Employees WHERE first_name LIKE '%sha%';


-- 20. Display information of employees whose second position of first_name contains letter ‘o’  
SELECT * FROM Employees WHERE first_name LIKE '_o%';


-- 21. Display the information of employees whose third position of first_name contains the letter ‘s’  
SELECT * FROM Employees WHERE first_name LIKE '__s%';


-- 22. Display information of employees which have first_name of at least six characters  
SELECT * FROM Employees WHERE first_name LIKE '______%';


-- 23. Display the information of employees whose first_name begins with a,k,m,s,r  
-- ^   → Match at the START of string
SELECT * FROM Employees WHERE first_name REGEXP '^[akmsr]';


-- 24. Display information of employees whose first_name begins with [a-s] and ends with l  
SELECT * FROM Employees WHERE first_name REGEXP '^[a-s].*l$';


-- 25. Display information of employees whose first_name does not start with d but ends with h  
SELECT * FROM Employees WHERE first_name REGEXP '^[^d].*h$';


-- ==================== DISTINCT ===================  
-- 26. Display the different position available for employee  
SELECT DISTINCT position FROM Employees;


-- 27. List out the unique address available for employee table  
SELECT DISTINCT address FROM Employees;


-- 28. List out the employee who have unique first_name and address  
SELECT DISTINCT first_name,address  FROM Employees;




-- ================================ AS =========================  
-- 29. Write a query to get first_name,last_name, ssf of all employees. ssf is calculated as 31% of salary  
SELECT first_name,last_name, salary*1.31 AS ssf FROM Employees;


-- 30. Write a query to get the employee_id, name (first_name, last_name), location (address) from employee  
SELECT employee_id, CONCAT(first_name,' ',last_name) AS name, address AS location FROM Employees;



-- ============================ ORDER BY ===========================  
-- 31. Display the information of employees in ascending order by address  
SELECT * FROM Employees ORDER BY address ASC;

-- 32. Display the information of employees in descending order by address  
SELECT * FROM Employees ORDER BY address DESC;

-- 33. Display the information of employees in ascending order by address and department  
SELECT * FROM Employees ORDER BY address,department ASC;


-- * in SELECT * = all columns  ,  in COUNT(*) = all rows
SELECT COUNT(*) FROM Employees;
-- ====================== Aggregate functions ======================  
-- 34. Count the number of employees  
SELECT COUNT(DISTINCT employee_id) FROM Employees;


-- 35. Count the number of unique first_name of employees  
SELECT COUNT(DISTINCT first_name ) FROM Employees;


-- 36. To get the number of different number of positions available for employees table  
SELECT COUNT( DISTINCT position) FROM Employees;


-- 37. To get the total salaries payable to employees.  
SELECT SUM(salary) FROM Employees;


-- 38. Find the average salary of employees  
SELECT AVG(salary) FROM Employees;


-- 39. Find the minimum salary of employees  
SELECT MIN(salary) FROM Employees;


-- 40. Display first_name, last_name of employees with highest salary  
SELECT first_name,last_name FROM Employees WHERE salary=(SELECT MAX(salary) FROM Employees);


-- 41. Display first_name,last_name,department,position whose salary is less than average salary of all employees  
SELECT first_name,last_name,department,position FROM Employees WHERE salary<(SELECT AVG(salary) FROM Employees); 




-- ===================== GROUP BY and HAVING clause ==========================  
-- 42. Find the average salary of employees in each department  
/* FROM Employees
   ↓
GROUP BY department (γ)
   ↓
AVG(salary) aggregation
   ↓
π department, average_salary  */

SELECT AVG(salary)  AS Average_Salaries FROM Employees GROUP BY department;



-- 43. Find the average salary of employees for each position  
SELECT AVG(salary) AS Average_Salaries FROM Employees GROUP BY position;


-- 44. Find the department with their average salary greater than 60000  
-- WHERE → filters rows before grouping.
-- HAVING → filters groups after aggregation (used with group by & aggregate functions bcz where clause cannot work here directly)
-- FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
SELECT department, AVG(salary) FROM Employees
GROUP BY department 
HAVING AVG(salary)>60000;

-- 45. Find the position of the employee in which average salary of position is greater than 60000  
SELECT position, AVG(salary) FROM Employees
GROUP BY position
HAVING AVG(salary)>60000;




-- ====================== Subquery ======================  
-- 46. Display information of employee whose salary is greater than average salary of all employees  
SELECT * FROM Employees WHERE salary>(SELECT AVG(salary) FROM Employees);


-- 47. Display information of employee whose salary is greater than at least one employee of finance department.  
-- > SOME or ANY =  means "greater than at least one".
-- > ALL(...) = "greater than all values".
SELECT *  FROM Employees  WHERE salary > SOME (SELECT DISTINCT salary FROM Employees WHERE department = 'finance'); 


-- 48. Display information of employee whose salary is greater than that of all employees of finance department.  
SELECT * FROM Employees WHERE salary> ALL(SELECT salary FROM Employees WHERE department = 'finance'); 


-- 49. Increase the salary of employees by 10% whose salary is greater than the average salary of all employees.  
UPDATE Employees 
SET salary = salary * 1.1 WHERE 
salary> (SELECT avg_salary 
    FROM (SELECT AVG(salary) AS avg_salary FROM Employees) AS temp);


-- 50. Delete the information of employees whose salary is less than average salary of all employees.  
DELETE FROM Employees WHERE salary<(SELECT AVG(salary) FROM Employees);

-- Solution: subquery ko ek derived table me wrap karna hoga:
DELETE FROM Employees
WHERE salary < (
    SELECT avg_salary 
    FROM (SELECT AVG(salary) AS avg_salary FROM Employees) AS temp
);


