-- 1. CREATE DATABASE AND USE IT
CREATE DATABASE customers_db;        -- Create a new database
USE customers_db;                    -- Switch to the newly created database


-- 2. CREATE TABLE customers WITH CONSTRAINTS
-- Method 1: Creating table with PRIMARY KEY and NOT NULL constraints
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,              -- Primary key (unique + not null)
    name VARCHAR(30) NOT NULL,                -- Name cannot be NULL
    email VARCHAR(255),                       -- Email (will make unique later)
    age INT,                                  -- Age (will add CHECK later)
    address VARCHAR(30)                       -- Address (will set default later)
);




-- 3. ADD MORE CONSTRAINTS AFTER TABLE CREATION
-- Make Email unique for each customer
ALTER TABLE customers 
ADD UNIQUE (email);

-- Ensure Age must be greater than 18
ALTER TABLE customers 
ADD CHECK (age>18);
-- ADD CONSTRAINT age_check CHECK (age>18);   -- CONSTRAINT IS WRITTEN SO THAT WE CAN GIVE IT A NAME OTHERWISE NO NEED SUCH AS ABOVE

-- Set default value for Address to 'bhaktapur'
ALTER TABLE customers 
ALTER address SET DEFAULT 'bhaktapur';

-- 4. INSERTING RECORDS (Testing Constraints)
INSERT INTO customers 
VALUES (1, 'ram', 'ram@gmail.com', 22, 'kathmandu');

INSERT INTO customers 
VALUES (2, 'sita', 'sita@gmail.com', 25, 'pokhara');

-- Violates PRIMARY KEY constraint (duplicate ID)
INSERT INTO customers 
VALUES (2, 'gita', 'gita@gmail.com', 26, 'butwal');          -- CHECK TABLE gita is not added due to constraint voilation

-- Violates NOT NULL constraint (missing 'name')
INSERT INTO customers (customer_id, email, age, address)
VALUES (3, 'gita@gmail.com', 26, 'butwal');

-- Valid insertion
INSERT INTO customers 
VALUES (4, 'hari', 'hari@gmail.com', 27, 'lalitpur');

-- Violates CHECK constraint (age must be >18)
INSERT INTO customers 
VALUES (11, 'ganesh', 'ganesh@gmail.com', 15, 'dolkha');

-- Violates UNIQUE constraint (duplicate email)
INSERT INTO customers 
VALUES (16, 'ramesh', 'ram@gmail.com', 24, 'chitwan');

-- Tests DEFAULT constraint (no address provided)
INSERT INTO customers (customer_id, name, email, age)
VALUES (5, 'gopal', 'gopal@gmail.com', 20);

-- View all records in customers table
SELECT * FROM customers;



-- 5. CREATE TABLE orders WITH FOREIGN KEY CONSTRAINT
CREATE TABLE orders (
    order_id INT PRIMARY KEY,                         -- Primary key for orders
    product_name VARCHAR(30),                         -- Product name
    price INT,                                        -- Product price
    customer_id INT,                                  -- Foreign key reference
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    -- Links order.customer_id → customers.customer_id
);


-- 6. UPDATE RECORD AND INSERT INTO orders TABLE
-- Update name of customer where ID = 3
UPDATE customers 
SET name = 'gita' 
WHERE customer_id = 3;


-- Insert valid records into orders table
INSERT INTO orders VALUES (1, 'iron', 1200, 1);
INSERT INTO orders VALUES (2, 'guitar', 4500, 2);
INSERT INTO orders VALUES (3, 'phone', 57000, 1);
INSERT INTO orders VALUES (4, 'printer', 88000, 3);
INSERT INTO orders VALUES (5, 'drone', 125000, 2);
INSERT INTO orders VALUES (6, 'smartwatch', 7500, 4);
INSERT INTO orders VALUES (7, 'oven', 14500, 5);

-- Violates FOREIGN KEY constraint (customer_id=6 doesn’t exist)
INSERT INTO orders VALUES (8, 'Laptop', 158000, 6);

-- View all records in orders table
SELECT * FROM orders;


-- DROP DATABASE customers_db;



