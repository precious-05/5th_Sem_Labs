-- 1. Create a database named eemcDB  (DDL)
CREATE DATABASE eemcDB;

-- Select the database to use
USE eemcDB;

-- 2. Create table named student_info in database eemcDB 
--    with following columns and datatypes: 
--    sid (INT), name (VARCHAR(50)), contact (CHAR(10)), 
--    faculty (VARCHAR(50)), college_name (VARCHAR(50))  (DDL)
CREATE TABLE student_info (
   sid INT,
   name VARCHAR(50),
   contact CHAR(10),
   faculty VARCHAR(50),
   college_name VARCHAR(50)
);

-- 3. Now add column named address with datatype VARCHAR(30) (DDL)
ALTER TABLE student_info
ADD address VARCHAR(30);

-- 4. Delete the column named contact (DDL)
ALTER TABLE student_info
DROP COLUMN contact;

-- 5. Rename column named address as location (DDL)
ALTER TABLE student_info
CHANGE COLUMN address location VARCHAR(30);

-- 6. Change data type of faculty to CHAR(20) (DDL)
ALTER TABLE student_info
MODIFY faculty CHAR(20);

-- 7. Insert minimum 10 information of students into table student_info (DML)
--    Conditions:
--    - Insert 1 student whose faculty is not known
--    - Insert 1 student whose college_name is not known

INSERT INTO student_info (sid, name, faculty, college_name, location)
VALUES (1, 'Ali Khan', 'CS', 'EEMC', 'Lahore');

INSERT INTO student_info VALUES (2, 'Sara Ali', 'Math', 'EEMC', 'Karachi');
INSERT INTO student_info VALUES (3, 'Ram', 'Physics', 'EEMC', 'Kathmandu');
INSERT INTO student_info VALUES (4, 'Bilal', 'Civil', 'EEMC', 'Pokhara');
INSERT INTO student_info VALUES (5, 'Ayesha', 'CS', 'EEMC', 'Lahore');
INSERT INTO student_info VALUES (6, 'Imran', 'Electrical', 'EEMC', 'Multan');
INSERT INTO student_info VALUES (7, 'Hina', 'IT', 'EEMC', 'Islamabad');
INSERT INTO student_info VALUES (8, 'Nida', 'Biology', 'EEMC', 'Faisalabad');
INSERT INTO student_info VALUES (9, 'Usman', NULL, 'EEMC', 'Karachi');   -- faculty not known
INSERT INTO student_info VALUES (10, 'Zara', 'CS', NULL, 'Lahore');      -- college_name not known

-- 8. Update the information of student whose sid=3 by setting faculty='Civil' (DML)
UPDATE student_info
SET faculty = 'Civil'
WHERE sid = 3;

-- 9. Update the information of student whose name='Ram' 
--    and location='Kathmandu' by setting faculty='Computer' (DML)
UPDATE student_info
SET faculty = 'Computer'
WHERE name = 'Ram' AND location = 'Kathmandu';

-- 10. Delete the information of student whose faculty='Civil' 
--     and location='Pokhara' (DML)
DELETE FROM student_info
WHERE faculty = 'Civil' AND location = 'Pokhara';

-- 11. Display all the information of students (DML - SELECT)
SELECT * FROM student_info;

-- 12. Display name and faculty of students whose location is 'Kathmandu' (DML - SELECT)
SELECT name, faculty
FROM student_info
WHERE location = 'Kathmandu';

-- 13. Display name and faculty of students whose location is 'Pokhara' 
--     and college_name='EEMC' (DML - SELECT)
SELECT name, faculty
FROM student_info
WHERE location = 'Pokhara' AND college_name = 'EEMC';

-- 14. Delete all rows from table (DML)
DELETE FROM student_info;

-- 15. Delete the table named student_info (DDL)
DROP TABLE student_info;

-- 16. Delete the database named eemcDB (DDL)
DROP DATABASE eemcDB;
