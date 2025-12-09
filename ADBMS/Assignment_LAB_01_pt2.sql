-- =========================================
-- Question 2
-- Retrieve all columns from the customer table without using '*'. 
-- Sort the results based on the highest to lowest balance and last name from lowest to highest.
SELECT id, last_name, first_name, initial, areacode, phone, balance FROM customer
ORDER BY balance DESC, last_name ASC;

-- =========================================
-- Question 3
-- Retrieve the id and name of all vendors. 
-- Use a vendor_name as the alias for the vendor name.
SELECT id, name AS vendor_name FROM vendor;

-- =========================================
-- Question 4
-- Retrieve the description and price of all products. 
-- Calculate quantity - minimum_quantity AS surplus and sort surplus from highest to lowest.
SELECT description, price, quantity - minimum_quantity AS surplus FROM product ORDER BY surplus DESC;

-- =========================================
-- Question 5
-- Retrieve the total balance of all customers.
SELECT SUM(balance) FROM customer;

-- =========================================
-- Question 6
-- Retrieve the names of all customers whose balance is greater than $500.
SELECT CONCAT(first_name,' ',last_name) AS Customer_Name FROM customer WHERE balance>500;

-- =========================================
-- Question 7
-- Retrieve the total price for each invoice.
SELECT SUM(units * price) AS Total_Price FROM line GROUP BY invoice_id;


-- =========================================
-- Question 8
-- Retrieve the vendor id, vendor name and total quantity of all products. 
-- Calculate the quantity * price as total_cost.
SELECT v.id, v.name,SUM(p.quantity), SUM(p.quantity * p.price) AS Total_Cost
FROM vendor v
INNER JOIN product p
ON v.id=p.vendor_id
GROUP BY v.id, v.name;

-- =========================================
-- Question 9
-- Retrieve the total quantity and price for each product.
SELECT code, SUM(quantity) AS total_quantity, SUM(quantity * price) AS total_price
FROM product GROUP BY code;


-- =========================================
-- Question 10
-- Retrieve the total number of invoices for each customer, 
-- including customers that have not made a purchase.
SELECT c.id, c.first_name, c.last_name, COUNT(i.id) AS Total_Invoices
FROM CUSTOMER c
LEFT JOIN INVOICE i ON c.id = i.customer_id
GROUP BY c.id, c.first_name, c.last_name;



-- =========================================
-- Question 11
-- Retrieve the total number of products each vendor sells.
SELECT v.id,v.name, COUNT(p.code) AS Total_Products FROM vendor v 
LEFT JOIN product p ON v.id=p.vendor_id
GROUP BY v.id,v.name;

-- =========================================
-- Question 12
-- Average balance of customers by state
-- Note: Customers table has no state, so we assume grouping by areacode
SELECT areacode, AVG(balance) AS avg_balance
FROM customer
GROUP BY areacode;

-- =========================================
-- Question 13
-- Customer with the highest balance
SELECT id, CONCAT(first_name, ' ', last_name) AS customer_name, balance
FROM customer
ORDER BY balance DESC
LIMIT 1;

-- =========================================
-- Question 14
-- Vendor who sells the most expensive product
SELECT v.id AS vendor_id, v.name AS vendor_name, MAX(p.price) AS max_price
FROM vendor v
JOIN product p ON v.id = p.vendor_id
GROUP BY v.id, v.name
ORDER BY max_price DESC
LIMIT 1;

-- =========================================
-- Question 15
-- Top 3 customers with highest total balance
SELECT id, CONCAT(first_name, ' ', last_name) AS customer_name, balance
FROM customer
ORDER BY balance DESC
LIMIT 3;



