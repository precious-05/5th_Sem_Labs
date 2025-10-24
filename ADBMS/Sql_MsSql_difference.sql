CREATE DATABASE example;
use example;
CREATE TABLE emp_time (
    eid VARCHAR(10),
    name VARCHAR(30),
    start_time TIME,
    end_time TIME
);

INSERT INTO emp_time VALUES
('E101', 'Hari', '09:00:00', '17:00:00'),
('E102', 'Malati', '08:30:00', '15:45:00'),
('E103', 'Kalyan', '10:00:00', '18:30:00');

-- TIMEDIFF() returns a TIME string like '08:00:00' not numeric
SELECT name, TIMEDIFF(end_time, start_time) AS total_work_time
FROM emp_time;

-- To calculate average hours, we must convert TIME to SECONDS to HOURS
SELECT 
    AVG(TIME_TO_SEC(TIMEDIFF(end_time, start_time)) / 3600) AS avg_hours
FROM emp_time;





-- In MS SQL Server, DATEDIFF() directly returns numeric values
-- No need for TIME_TO_SEC() or manual conversion 👇

-- Show total work hours for each employee
SELECT 
    name,
    DATEDIFF(HOUR, start_time, end_time) AS total_work_hours
FROM emp_time;

-- 2️⃣ Calculate average working hours directly (numeric result)
SELECT 
    AVG(DATEDIFF(MINUTE, start_time, end_time) / 60.0) AS avg_working_hours
FROM emp_time;

--  Explanation:
-- In MySQL → TIMEDIFF() = '08:00:00' (string)
--             must convert: TIME_TO_SEC() / 3600 to get hours
-- In MS SQL → DATEDIFF(HOUR, start, end) gives numeric result (8, 7, etc.)
--             no conversion needed 



DROP database example;