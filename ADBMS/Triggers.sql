-- Trigger ek automatic program hota hai jo tab chalta hai jab koi specific event (INSERT, UPDATE, DELETE) kisi table par hoti hai
-- Agar hmary "Items" table mn kisi product ka stock update hota hai, aur hm chahen k agar stock 5 se kam ho jaye to automatically
-- "Orders" table mn ek new order record insert ho jaye to ye kaam trigger karega


CREATE DATABASE Inventory;
USE Inventory;
-- Step 1:
-- Create a table named "Items" to store item details such as 
-- item ID, name, inventory level, and minimum stock level.
CREATE TABLE Items (
    ItemID INT PRIMARY KEY,
    ItemName VARCHAR(50),
    InventoryLevel INT,
    MinimumLevel INT
);

-- Step 2:
-- Insert some sample records into the "Items" table to represent 
-- the current stock levels and minimum required levels of items.
INSERT INTO Items (ItemID, ItemName, InventoryLevel, MinimumLevel)
VALUES 
(1, 'Item A', 10, 5),
(2, 'Item B', 8, 6),
(3, 'Item C', 15, 10);


-- Step 3:
-- Create another table named "Orders" to store records of 
-- automatically generated orders whenever stock falls below 
-- the minimum level.
CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    ItemID INT,
    Quantity INT,
    OrderDate DATE
);



-- Step 4:
-- Create a trigger named "check_inventory_level" on the "Items" table.
-- The trigger will execute AFTER an UPDATE event.
-- It will compare the current inventory level with the minimum level.
-- If the inventory falls below the minimum level, 
-- it will automatically insert a new order record into the "Orders" table.



/*CREATE [OR REPLACE] TRIGGER trigger_name  
{BEFORE | AFTER} {INSERT | UPDATE | DELETE}  
ON table_name  
[FOR EACH ROW]  
[WHEN (condition)]  
BEGIN  -- Trigger body: SQL statements or code  
END; */

DELIMITER //
CREATE TRIGGER check_inventory_level
AFTER UPDATE ON Items
FOR EACH ROW   -- ROW LEVEL TRIGGER
BEGIN
	DECLARE current_inventory INT;
    DECLARE minimum_level INT;
    
	SET current_inventory = NEW.InventoryLevel;   -- NEW.InventoryLevel → us row ka updated inventory level
    SET minimum_level = NEW.MinimumLevel;  -- NEW.MinimumLevel → us row ka updated minimum level
    -- NEW.ItemID → usi row ka ItemID (jo Items table me already hai)
    IF current_inventory<minimum_level THEN
		INSERT INTO Orders (ItemID, Quantity, OrderDate)
        VALUES (NEW.ItemID, (minimum_level - current_inventory), CURDATE());  -- CURDATE() is a built-in MySQL function that returns the current date (today’s date) from the system.
	END IF;                      
END //
DELIMITER ;




/*The following trigger will also work     
CREATE TRIGGER check_inventory_level
AFTER UPDATE ON Items
FOR EACH ROW
BEGIN
    IF NEW.InventoryLevel < NEW.MinimumLevel THEN
        INSERT INTO Orders (ItemID, Quantity, OrderDate)
        VALUES (NEW.ItemID, (NEW.MinimumLevel - NEW.InventoryLevel), CURDATE());
    END IF;
END;
*/

-- Step 5:
-- Update inventory levels of some items to test the trigger.
-- For example, reduce Item A's stock below its minimum level 
-- to check if the trigger generates a new order automatically.
UPDATE Items
SET InventoryLevel = 3
WHERE ItemID = 1;   -- Item A falls below minimum level

UPDATE Items
SET InventoryLevel = 4
WHERE ItemID = 2;   -- Item B remains above minimum level

-- Step 6:
-- Display all records from the "Orders" table using a SELECT statement 
-- to verify that the trigger worked correctly.
SELECT * FROM Orders;
SELECT * FROM Items;



-- DROP DATABASE Inventory;

-- ======================= DISCUSSION =========================
-- After updating Item A’s stock, the trigger automatically inserted 
-- a new record into the "Orders" table because its inventory 
-- was below the defined minimum level.
-- For Item B, no order was created since its inventory was still above the minimum level.

-- ======================= CONCLUSION =========================
-- Triggers help automate repetitive or conditional tasks in a database.
-- They ensure data integrity and can perform actions such as generating 
-- alerts, inserting logs, or maintaining consistency across tables.

-- *********************** THE END ****************************





























