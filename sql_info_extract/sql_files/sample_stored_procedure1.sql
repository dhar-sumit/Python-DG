-- sql_files/sample_stored_procedure1.sql

-- Create a table
CREATE TABLE Employees (
    EmpID INT PRIMARY KEY,
    EmpName VARCHAR(100),
    DeptID INT,
    Salary DECIMAL(10,2)
);

-- Insert some data
INSERT INTO Employees (EmpID, EmpName, DeptID, Salary)
VALUES (1, 'Emp 1', 101, 60000);

INSERT INTO Employees (EmpID, EmpName, DeptID, Salary)
VALUES (2, 'Emp 2', 102, 45000);

INSERT INTO Employees (EmpID, EmpName, DeptID, Salary)
VALUES (3, 'Emp 3', 103, 47000);

INSERT INTO Employees (EmpID, EmpName, DeptID, Salary)
VALUES (4, 'Emp 4', 104, 50000);

INSERT INTO Employees (EmpID, EmpName, DeptID, Salary)
VALUES (5, 'Emp 5', 105, 74000);

-- Update data
UPDATE Employees
SET Salary = 65000
WHERE EmpID = 3;

-- Delete data
DELETE FROM Employees
WHERE EmpID = 4;

-- Create a stored procedure
CREATE PROCEDURE GetEmployeeDetails
    @EmpID INT,
    @DeptID INT
AS
BEGIN
    SELECT EmpID, EmpName, Salary
    FROM Employees
    WHERE EmpID = @EmpID AND DeptID = @DeptID;
END;

-- Create a view
CREATE VIEW HighSalaryEmployees AS
SELECT EmpID, EmpName, Salary
FROM Employees
WHERE Salary > 50000;
