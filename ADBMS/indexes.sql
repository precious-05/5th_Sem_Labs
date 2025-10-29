CREATE DATABASE index_demo;
USE index_demo;
CREATE TABLE students (
  student_id INT PRIMARY KEY,        -- Primary Index (auto)
  name VARCHAR(50),
  city VARCHAR(50),
  email VARCHAR(100),
  bio TEXT
);
-- student_id default primary index (Clustered Index in InnoDB)
-- name, city, email, bio (No index columns)
INSERT INTO students VALUES
(1, 'Ayesha', 'Lahore', 'ayesha@gmail.com', 'A computer science student'),
(2, 'Bilal', 'Karachi', 'bilal@yahoo.com', 'Interested in web development'),
(3, 'Fatima', 'Islamabad', 'fatima@gmail.com', 'Likes databases and data analysis'),
(4, 'Ahmed', 'Lahore', 'ahmed@hotmail.com', 'Learning backend systems'),
(5, 'Hira', 'Multan', 'hira@gmail.com', 'Frontend designer and artist');

SHOW INDEXES FROM students;


-- Simple (Single-Column) Index
CREATE INDEX idx_city ON students(city);
SHOW INDEXES FROM students;
-- It will retrieve faster
SELECT * FROM students WHERE city='Lahore';

CREATE UNIQUE INDEX idx_email ON students(email);
-- Ensuring no 2 students have same email
SHOW INDEXES FROM students;

-- Composite Index (Multi-column)
CREATE INDEX idx_name_city ON students(name, city);
SHOW INDEXES FROM students;
-- But order matters it helps when name is used first in query condition
SELECT * FROM students WHERE name='Ahmed' AND city='Lahore';

-- . Fulltext Index (Used for searching words inside long text columns — e.g. in bio)
CREATE FULLTEXT INDEX idx_bio ON students(bio);
SELECT * FROM students WHERE MATCH(bio) AGAINST('database');

-- DROP INDEX idx_bio on students;
