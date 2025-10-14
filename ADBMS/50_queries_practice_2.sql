USE Company;




-- ===================== Arithmetic, Logical & Relational Operators =====================

-- 1. Display the first_name and last_name of employee whose department is finance  
SELECT first_name, last_name FROM Employees WHERE department='finance';

-- 2. Display all the information of employees whose address is not kathmandu  
SELECT * FROM Employees WHERE address!='kathmandu';

-- 3. Increment the salary of all employees by 15%  
UPDATE Employees SET salary=salary*1.15;
 
-- 4. Decrease the salary of manager by 5%  
UPDATE Employees SET salary=salary*0.95;

-- 5. Delete information of employees whose age is less than 18  
DELETE FROM Employees WHERE age<18;

-- 6. Display the position of employees whose salary is greater than or equals to 50000  
SELECT DISTINCT position FROM Employees WHERE salary>=50000;

-- 7. Display information of employees whose position is manager and address is kathmandu  
SELECT * FROM Employees WHERE position='manager' AND address='kathmandu';

-- 8. Display information of employee who either live in pokhara or kathmandu but age is greater than 25  
SELECT * FROM Employees WHERE (address='pokhara' OR address='kathmandu') AND age>25;

-- 9. Display first_name, last_name, and position of employees whose salary is in the range of 70000 to 80000  
SELECT first_name, last_name, position FROM Employees WHERE salary BETWEEN 70000 AND 80000;

-- 10. Display first_name, last_name, and position of employees whose salary is not in the range of 70000 to 80000 
SELECT first_name, last_name,position FROM Employees WHERE salary NOT BETWEEN 70000 AND 80000; 

-- 11. Display the information of employees whose salary is equal to 69000,30000,35000,40000,71300,80500  
SELECT * FROM Employees WHERE salary IN(69000,30000,35000,40000,71300,80500); 


-- 12. Display information of employees whose department is (sales, purchase) but not salary equal to (69000,71300,80500)  
SELECT * FROM Employees WHERE department IN ('sales', 'purchase') AND salary NOT IN(69000,71300,80500); 






-- ===================== LIKE Operator with Wildcards =====================

-- 13. Display information of employees whose first_name starts with letter ‘a’  
SELECT * FROM Employees WHERE first_name LIKE "a%";

-- 14. Display information of employees whose first_name starts with letter ‘ro’  
SELECT * FROM Employees WHERE first_name LIKE "ro%";

-- 15. Display information of employees whose last_name ends with letter ‘el’  
SELECT * FROM Employees WHERE last_name LIKE "%el";

-- 16. Display information of employees whose first_name has exactly six characters  
SELECT * FROM Employees WHERE first_name LIKE "______";

-- 17. Display information of employees whose first_name starts with r and has exactly six characters  
SELECT * FROM Employees WHERE first_name LIKE "r_____";

-- 18. Display the information of employees which contains substring ‘sha’ in first_name  
SELECT * FROM Employees WHERE first_name LIKE "%sha%";

-- 19. Display information of employees whose second position of first_name contains letter ‘o’ 
SELECT * FROM Employees WHERE  first_name LIKE "_o%";
 
-- 20. Display the information of employees whose third position of first_name contains letter ‘s’  
SELECT * FROM Employees WHERE first_name LIKE "__s%";

-- 21. Display information of employees which have first_name of at least six characters  
SELECT * FROM Employees WHERE first_name LIKE "______%";


-- 22. Display the information of employees whose first_name begins with a,k,m,s,r (using REGEXP)  
SELECT * FROM Employees WHERE first_name REGEXP "^[akmsr]";

-- 23. Display information of employees whose first_name begins with [a-s] and ends with l (using REGEXP) 
SELECT * FROM Employees WHERE first_name REGEXP "^[a-s].*l$";
 
-- 24. Display information of employees whose first_name does not start with d but ends with h (using REGEXP)  
SELECT * FROM Employees WHERE first_name REGEXP "^[^d].*h$";







-- ===================== DISTINCT Keyword =====================

-- 25. Display the different positions available for employees  
SELECT DISTINCT position FROM Employees;

-- 26. List out the unique addresses from employee table  
SELECT DISTINCT address FROM Employees;

-- 27. List out the employees who have unique first_name and address
SELECT DISTINCT first_name, address FROM Employees;



-- ===================== AS (Aliases) =====================

-- 28. Write a query to get first_name, last_name, and ssf (31% of salary) of all employees  
SELECT first_name, last_name, salary*1.31 AS ssf FROM Employees;

-- 29. Write a query to get employee_id, full name (first_name + last_name), and location (address)  
SELECT employee_id, CONCAT(first_name, ' ' ,last_name) AS Employee_Name , address AS location FROM Employees;


-- ===================== ORDER BY =====================

-- 30. Display information of employees in ascending order by address  
SELECT * FROM Employees ORDER BY address  ASC;

-- 31. Display information of employees in descending order by address  
SELECT * FROM Employees ORDER BY address  DESC;

-- 32. Display information of employees in ascending order by address and department  
SELECT * FROM Employees ORDER BY address , department ASC;


-- ===================== Aggregate Functions =====================

-- 33. Count the number of employees 
SELECT COUNT(*) FROM Employees;            -- USING AGGREGATE METHOD COUNT
SELECT COUNT(DISTINCT employee_id) FROM Employees;   -- 2ND METHOD TRIED OWN MY OWN


-- 34. Count the number of unique first_name of employees  
SELECT COUNT(DISTINCT first_name)  FROM Employees;

-- 35. Count the number of different positions available 
SELECT COUNT(DISTINCT position)  FROM Employees;
 
-- 36. Get the total salaries payable to employees  
SELECT SUM(salary) FROM Employees;

-- 37. Find the average salary of employees  
SELECT AVG(salary) FROM Employees;

-- 38. Find the minimum salary of employees  
SELECT MIN(salary) FROM Employees;

-- 39. Display first_name and last_name of employees with highest salary  
SELECT first_name,last_name FROM Employees WHERE salary=(SELECT MAX(salary) FROM Employees);

-- 40. Display first_name, last_name, department, position of employees whose salary < average salary  
SELECT first_name, last_name, department, position FROM Employees WHERE salary < (SELECT AVG(salary) FROM Employees);



/*When to Use GROUP BY

✅ Jab multiple rows ko group krna ho (e.g., per department, per city).

✅ Jab query mn aggregate function (AVG, SUM, COUNT, etc.) + normal column(s) dono select hoon.

✅ Jab har group ka separate result chahiye (like average salary per department).

✅ Jab output mn ek column group identifier (e.g., department name) aur aggregate value dono hoon.


When to Use a Subquery

✅ Jab comparison ya filtering krni ho using aggregate value.

✅ Jab overall table ka ek single value chahiye (e.g., total, max, avg, etc.).

✅ Jab row-wise comparison krni ho us single value k sath.

✅ Jab GROUP BY ki need na ho (kyun k sirf 1 value mil rhi hoti hai).
Row-wise comparison with a single aggregate value is not possible using GROUP BY — it’s done using a subquery.*/

-- ===================== GROUP BY and HAVING =====================
-- HAVING → filters groups after aggregation (used with group by & aggregate functions bcz where clause cannot work here directly)

-- 41. Find the average salary of employees in each department  
SELECT department,AVG(salary) FROM Employees GROUP BY department;

-- 42. Find the average salary of employees for each position 
SELECT position,AVG(salary) AS Average_Salaries FROM Employees GROUP BY position;
 
-- 43. Find departments with average salary greater than 60000
SELECT department,AVG(salary) FROM Employees GROUP BY department HAVING AVG(salary)>60000 ;
  
-- 44. Find positions with average salary greater than 60000  
SELECT position, AVG(salary) FROM Employees GROUP BY position HAVING AVG(salary)>60000 ;


-- ===================== Subqueries =====================

-- 45. Display information of employees whose salary is greater than average salary  
SELECT * FROM Employees WHERE salary>(SELECT AVG(salary) FROM Employees);

-- 46. Display information of employees whose salary is greater than at least one employee of finance dept 
SELECT * FROM Employees WHERE salary> SOME ( SELECT DISTINCT salary FROM Employees WHERE department='finance');
 
-- 47. Display information of employees whose salary is greater than all employees of finance dept 
SELECT * FROM Employees WHERE salary> ALL ( SELECT DISTINCT salary FROM Employees WHERE department='finance');

-- 48. Increase the salary by 10% for employees whose salary is greater than average salary  
UPDATE Employees SET salary=salary*1.1 WHERE salary>(SELECT avg_salary FROM (SELECT AVG(salary) AS avg_salary FROM Employees) AS temp);

-- 49. Delete employees whose salary is less than average salary  
DELETE FROM Employees WHERE salary<( SELECT avg_salary FROM (SELECT AVG(salary) AS avg_salary FROM Employees) AS temp);
