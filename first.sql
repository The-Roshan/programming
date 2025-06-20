-- Introduction to SQL and creating a database
CREATE DATABASE SchoolDB;
USE SchoolDB;

-- SQL Data Types and Data Definition Language (DDL)
CREATE TABLE Students (
    StudentID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Email VARCHAR(100)
);

CREATE TABLE Courses (
    CourseID INT PRIMARY KEY,
    CourseName VARCHAR(100),
    Credits INT
);

CREATE TABLE Enrollments (
    EnrollmentID INT PRIMARY KEY,
    StudentID INT,
    CourseID INT,
    EnrollmentDate DATE,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- Data Manipulation Language (DML)
-- Inserting data into Students table
INSERT INTO Students (StudentID, FirstName, LastName, DateOfBirth, Email)
VALUES (1, 'John', 'Doe', '2000-01-01', 'john.doe@example.com'),
       (2, 'Jane', 'Smith', '2001-02-02', 'jane.smith@example.com');

-- Inserting data into Courses table
INSERT INTO Courses (CourseID, CourseName, Credits)
VALUES (101, 'Mathematics', 4),
       (102, 'Science', 3);

-- Inserting data into Enrollments table
INSERT INTO Enrollments (EnrollmentID, StudentID, CourseID, EnrollmentDate)
VALUES (1, 1, 101, '2023-09-01'),
       (2, 2, 102, '2023-09-01');

-- Selecting data
SELECT * FROM Students;
SELECT * FROM Courses;
SELECT * FROM Enrollments;

-- Updating data
UPDATE Students SET Email = 'john.newemail@example.com' WHERE StudentID = 1;

-- Deleting data
DELETE FROM Enrollments WHERE EnrollmentID = 2;

-- Data Control Language (DCL)
-- Granting privileges
GRANT SELECT, INSERT, UPDATE ON Students TO user_name;

-- Revoking privileges
REVOKE SELECT, INSERT, UPDATE ON Students FROM user_name;

-- Transaction Control Language (TCL)
-- Starting a transaction
BEGIN TRANSACTION;

-- Performing some operations
INSERT INTO Students (StudentID, FirstName, LastName, DateOfBirth, Email)
VALUES (3, 'Alice', 'Brown', '2002-03-03', 'alice.brown@example.com');

-- Committing the transaction
COMMIT;

-- Rolling back a transaction
BEGIN TRANSACTION;
DELETE FROM Students WHERE StudentID = 3;
ROLLBACK;  -- This will undo the delete operation

-- Creating a view
CREATE VIEW StudentDetails AS
SELECT StudentID, FirstName, LastName, Email FROM Students;

-- Using the view
SELECT * FROM StudentDetails;

-- Creating an index
CREATE INDEX idx_lastname ON Students (LastName);

-- Creating a stored procedure
CREATE PROCEDURE GetStudentDetails
AS
SELECT * FROM Students;

-- Executing the stored procedure
EXEC GetStudentDetails;

-- Scalar (Non-Aggregate) SQL Functions
-- String Functions
SELECT CONCAT(FirstName, ' ', LastName) AS FullName FROM Students;
SELECT UPPER(FirstName) AS UpperFirstName FROM Students;

-- Numeric Functions
SELECT ROUND(123.456, 2) AS RoundedValue;
SELECT ABS(-123) AS AbsoluteValue;

-- Date Functions
SELECT NOW() AS CurrentDateTime;
SELECT DATEADD(year, 1, '2023-01-01') AS NextYear;

-- Dropping the database (clean-up)
-- DROP DATABASE SchoolDB; -- Uncomment this line to drop the database
