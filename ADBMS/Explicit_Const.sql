-- ==========================================
--  TABLE: Department
-- ==========================================
-- Demonstrates: PRIMARY KEY + UNIQUE constraint
-- These avoid duplicate records and maintain entity integrity
-- Prevents: Insertion anomaly (no duplicate DeptIDs)
-- ==========================================

CREATE TABLE Department (
    DeptID INT PRIMARY KEY,              -- 🔹 PRIMARY KEY ensures each department is unique (Entity Integrity)
    DeptName VARCHAR(50) UNIQUE          -- 🔹 UNIQUE ensures no two departments have same name
);

-- Insert some departments
INSERT INTO Department VALUES (10, 'IT'), (20, 'HR'), (30, 'Finance');



-- ==========================================
-- 🌸 TABLE: Employee
-- ==========================================
-- Demonstrates: 
-- 1️⃣ PRIMARY KEY  (unique employee identity)
-- 2️⃣ FOREIGN KEY  (Referential Integrity → must match Department table)
-- 3️⃣ NOT NULL     (Entity Integrity → important fields must not be empty)
-- 4️⃣ CHECK        (Domain Constraint → restricts valid values)
-- 5️⃣ DEFAULT      (Automatic value when not provided)
-- ==========================================

CREATE TABLE Employee (
    EmpID INT PRIMARY KEY,                     -- Each employee uniquely identified → prevents duplicate or null IDs
    EmpName VARCHAR(50) NOT NULL,              -- Name can’t be NULL → ensures record completeness
    Gender CHAR(1) CHECK (Gender IN ('M','F')), -- Valid domain values only → prevents invalid data (Domain Constraint)
    Salary DECIMAL(10,2) CHECK (Salary > 0),    -- Salary must be positive → prevents logical update anomaly
    DeptID INT,                                -- Department to which employee belongs
    JoinDate DATE DEFAULT (CURRENT_DATE),       -- Automatically sets join date → reduces manual entry errors
    FOREIGN KEY (DeptID) REFERENCES Department(DeptID)
        ON DELETE SET NULL                      -- Referential Integrity → if department deleted, employee DeptID becomes NULL
);

-- Insert some valid data
INSERT INTO Employee (EmpID, EmpName, Gender, Salary, DeptID)
VALUES
(1, 'Aisha', 'F', 50000, 10),
(2, 'Bilal', 'M', 60000, 20),
(3, 'Sara', 'F', 55000, NULL);

-- Try inserting invalid data (for practice, uncomment and test one by one)
-- INSERT INTO Employee VALUES (1, 'DuplicateID', 'M', 40000, 10);      -- ❌ Violates PRIMARY KEY
-- INSERT INTO Employee VALUES (4, NULL, 'M', 40000, 10);               -- ❌ Violates NOT NULL
-- INSERT INTO Employee VALUES (5, 'Hassan', 'X', 40000, 10);           -- ❌ Violates CHECK (Gender domain)
-- INSERT INTO Employee VALUES (6, 'Ali', 'M', -20000, 10);             -- ❌ Violates CHECK (Salary domain)
-- INSERT INTO Employee VALUES (7, 'Fatima', 'F', 30000, 99);           -- ❌ Violates FOREIGN KEY (DeptID doesn’t exist)



-- ==========================================
-- 🌸 TABLE: Project
-- ==========================================
-- Demonstrates: Composite Key + Foreign Key combo
-- Helps avoid redundancy and ensures valid references
-- Prevents: Update anomaly (invalid project-employee pair)
-- ==========================================

CREATE TABLE Project (
    ProjectID INT,
    EmpID INT,
    HoursWorked INT CHECK (HoursWorked >= 0),
    PRIMARY KEY (ProjectID, EmpID),          -- Composite key → unique employee per project
    FOREIGN KEY (EmpID) REFERENCES Employee(EmpID)
        ON DELETE CASCADE                    -- If employee deleted → project records auto-removed (no orphan data)
);

-- Insert valid data
INSERT INTO Project VALUES
(101, 1, 5),
(101, 2, 7),
(102, 3, 4);



-- ==========================================
-- 🌸 TABLE: Attendance
-- ==========================================
-- Demonstrates DEFAULT + CHECK combo
-- Prevents wrong values or missing data
-- ==========================================

CREATE TABLE Attendance (
    EntryID INT AUTO_INCREMENT PRIMARY KEY,
    EmpID INT NOT NULL,
    AttendanceDate DATE DEFAULT (CURRENT_DATE),
    Status VARCHAR(10) CHECK (Status IN ('Present', 'Absent', 'Leave')),
    FOREIGN KEY (EmpID) REFERENCES Employee(EmpID)
);

-- Insert valid attendance
INSERT INTO Attendance (EmpID, Status)
VALUES
(1, 'Present'),
(2, 'Leave'),
(3, 'Absent');

