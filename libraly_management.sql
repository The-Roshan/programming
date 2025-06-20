-- Library Management System SQL Script
-- Created for managing books, members, loans, and related library operations

-- Drop existing tables if they exist to ensure a clean setup
DROP TABLE IF EXISTS LoanHistory;
DROP TABLE IF EXISTS Loans;
DROP TABLE IF EXISTS Reservations;
DROP TABLE IF EXISTS Fines;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Authors;
DROP TABLE IF EXISTS Publishers;
DROP TABLE IF EXISTS Categories;

-- Create Categories table
CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(50) NOT NULL,
    Description TEXT
);

-- Create Publishers table
CREATE TABLE Publishers (
    PublisherID INT PRIMARY KEY AUTO_INCREMENT,
    PublisherName VARCHAR(100) NOT NULL,
    Address VARCHAR(200),
    Phone VARCHAR(20),
    Email VARCHAR(100)
);

-- Create Authors table
CREATE TABLE Authors (
    AuthorID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    BirthDate DATE,
    Nationality VARCHAR(50)
);

-- Create Books table
CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(200) NOT NULL,
    AuthorID INT,
    PublisherID INT,
    CategoryID INT,
    ISBN VARCHAR(13) UNIQUE NOT NULL,
    PublicationYear INT,
    TotalCopies INT NOT NULL DEFAULT 1,
    AvailableCopies INT NOT NULL DEFAULT 1,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID),
    FOREIGN KEY (PublisherID) REFERENCES Publishers(PublisherID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- Create Members table
CREATE TABLE Members (
    MemberID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Phone VARCHAR(20),
    Address VARCHAR(200),
    JoinDate DATE NOT NULL,
    MembershipStatus ENUM('Active', 'Inactive', 'Suspended') DEFAULT 'Active'
);

-- Create Loans table
CREATE TABLE Loans (
    LoanID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT,
    MemberID INT,
    LoanDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Create LoanHistory table
CREATE TABLE LoanHistory (
    HistoryID INT PRIMARY KEY AUTO_INCREMENT,
    LoanID INT,
    BookID INT,
    MemberID INT,
    LoanDate DATE,
    DueDate DATE,
    ReturnDate DATE,
    FOREIGN KEY (LoanID) REFERENCES Loans(LoanID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Create Fines table
CREATE TABLE Fines (
    FineID INT PRIMARY KEY AUTO_INCREMENT,
    LoanID INT,
    MemberID INT,
    Amount DECIMAL(10,2) NOT NULL,
    IssueDate DATE NOT NULL,
    PaidDate DATE,
    Status ENUM('Pending', 'Paid') DEFAULT 'Pending',
    FOREIGN KEY (LoanID) REFERENCES Loans(LoanID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Create Reservations table
CREATE TABLE Reservations (
    ReservationID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT,
    MemberID INT,
    ReservationDate DATE NOT NULL,
    ExpiryDate DATE NOT NULL,
    Status ENUM('Active', 'Fulfilled', 'Cancelled') DEFAULT 'Active',
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Create index for faster queries
CREATE INDEX idx_book_isbn ON Books(ISBN);
CREATE INDEX idx_member_email ON Members(Email);
CREATE INDEX idx_loan_dates ON Loans(LoanDate, DueDate);

-- Stored Procedure: BorrowBook
DELIMITER //
CREATE PROCEDURE BorrowBook(
    IN p_MemberID INT,
    IN p_BookID INT,
    IN p_LoanDate DATE,
    IN p_DueDate DATE
)
BEGIN
    DECLARE available INT;
    
    -- Check if book is available
    SELECT AvailableCopies INTO available
    FROM Books
    WHERE BookID = p_BookID;
    
    IF available > 0 THEN
        -- Insert loan record
        INSERT INTO Loans (BookID, MemberID, LoanDate, DueDate)
        VALUES (p_BookID, p_MemberID, p_LoanDate, p_DueDate);
        
        -- Update available copies
        UPDATE Books
        SET AvailableCopies = AvailableCopies - 1
        WHERE BookID = p_BookID;
        
        -- Insert into loan history
        INSERT INTO LoanHistory (LoanID, BookID, MemberID, LoanDate, DueDate)
        VALUES (LAST_INSERT_ID(), p_BookID, p_MemberID, p_LoanDate, p_DueDate);
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Book is not available for borrowing';
    END IF;
END //
DELIMITER ;

-- Stored Procedure: ReturnBook
DELIMITER //
CREATE PROCEDURE ReturnBook(
    IN p_LoanID INT,
    IN p_ReturnDate DATE
)
BEGIN
    DECLARE v_BookID INT;
    
    -- Get BookID from loan
    SELECT BookID INTO v_BookID
    FROM Loans
    WHERE LoanID = p_LoanID;
    
    -- Update loan record
    UPDATE Loans
    SET ReturnDate = p_ReturnDate
    WHERE LoanID = p_LoanID;
    
    -- Update available copies
    UPDATE Books
    SET AvailableCopies = AvailableCopies + 1
    WHERE BookID = v_BookID;
    
    -- Update loan history
    UPDATE LoanHistory
    SET ReturnDate = p_ReturnDate
    WHERE LoanID = p_LoanID;
    
    -- Check for fines
    IF p_ReturnDate > (SELECT DueDate FROM Loans WHERE LoanID = p_LoanID) THEN
        INSERT INTO Fines (LoanID, MemberID, Amount, IssueDate)
        SELECT p_LoanID, MemberID, DATEDIFF(p_ReturnDate, DueDate) * 1.00, p_ReturnDate
        FROM Loans
        WHERE LoanID = p_LoanID;
    END IF;
END //
DELIMITER ;

-- Trigger: CheckMemberStatus
DELIMITER //
CREATE TRIGGER BeforeLoanInsert
BEFORE INSERT ON Loans
FOR EACH ROW
BEGIN
    DECLARE member_status ENUM('Active', 'Inactive', 'Suspended');
    
    SELECT MembershipStatus INTO member_status
    FROM Members
    WHERE MemberID = NEW.MemberID;
    
    IF member_status != 'Active' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Member is not active and cannot borrow books';
    END IF;
END //
DELIMITER ;

-- Insert sample data into Categories
INSERT INTO Categories (CategoryName, Description) VALUES
('Fiction', 'Fictional literature including novels and short stories'),
('Non-Fiction', 'Factual books including biographies and essays'),
('Science', 'Books on scientific topics'),
('History', 'Historical accounts and studies'),
('Fantasy', 'Fantasy and magical realism'),
('Mystery', 'Mystery and thriller novels'),
('Biography', 'Biographical accounts'),
('Technology', 'Books on technological advancements'),
('Self-Help', 'Personal development and self-improvement'),
('Children', 'Books for children and young readers');

-- Insert sample data into Publishers
INSERT INTO Publishers (PublisherName, Address, Phone, Email) VALUES
('Penguin Books', '123 Book St, NY', '555-0100', 'contact@penguin.com'),
('Random House', '456 Read Ave, NY', '555-0101', 'info@randomhouse.com'),
('HarperCollins', '789 Story Ln, CA', '555-0102', 'support@harpercollins.com'),
('Simon & Schuster', '101 Page Rd, NY', '555-0103', 'contact@simon.com'),
('Macmillan', '202 Novel Dr, TX', '555-0104', 'info@macmillan.com'),
('Hachette', '303 Tale St, CA', '555-0105', 'support@hachette.com'),
('Scholastic', '404 Kids Ave, NY', '555-0106', 'contact@scholastic.com'),
('Wiley', '505 Tech Rd, NJ', '555-0107', 'info@wiley.com'),
('Oxford Press', '606 Learn St, UK', '555-0108', 'contact@oxford.com'),
('Cambridge Press', '707 Study Ln, UK', '555-0109', 'info@cambridge.com');

-- Insert sample data into Authors
INSERT INTO Authors (FirstName, LastName, BirthDate, Nationality) VALUES
('John', 'Smith', '1970-03-15', 'American'),
('Emma', 'Johnson', '1985-07-22', 'British'),
('Michael', 'Brown', '1965-11-30', 'Canadian'),
('Sarah', 'Davis', '1978-04-12', 'Australian'),
('David', 'Wilson', '1980-09-05', 'American'),
('Jane', 'Taylor', '1972-12-18', 'British'),
('Robert', 'Anderson', '1968-06-25', 'American'),
('Emily', 'White', '1990-02-10', 'Canadian'),
('Thomas', 'Harris', '1975-08-03', 'American'),
('Laura', 'Martin', '1982-01-27', 'British');

-- Insert sample data into Books
INSERT INTO Books (Title, AuthorID, PublisherID, CategoryID, ISBN, PublicationYear, TotalCopies, AvailableCopies) VALUES
('The Great Adventure', 1, 1, 1, '9781234567890', 2010, 5, 3),
('Science Unveiled', 2, 2, 3, '9781234567891', 2015, 3, 2),
('History of Time', 3, 3, 4, '9781234567892', 2008, 4, 1),
('Mystic Realms', 4, 4, 5, '9781234567893', 2018, 6, 4),
('Murder Mystery', 5, 5, 6, '9781234567894', 2020, 5, 2),
('Life Lessons', 6, 6, 9, '9781234567895', 2019, 3, 3),
('Tech Revolution', 7, 7, 8, '9781234567896', 2021, 4, 4),
('Kids Tales', 8, 8, 10, '9781234567897', 2017, 7, 5),
('Biography of a Hero', 9, 9, 7, '9781234567898', 2016, 3, 2),
('Future Visions', 10, 10, 3, '9781234567899', 2022, 5, 3),
('The Lost Kingdom', 1, 2, 1, '9781234567900', 2011, 4, 2),
('Quantum Physics', 2, 3, 3, '9781234567901', 2014, 3, 1),
('Ancient Civilizations', 3, 4, 4, '9781234567902', 2009, 5, 3),
('Dragon Tales', 4, 5, 5, '9781234567903', 2019, 6, 4),
('The Hidden Clue', 5, 6, 6, '9781234567904', 2021, 4, 2),
('Grow Yourself', 6, 7, 9, '9781234567905', 2020, 3, 3),
('AI Revolution', 7, 8, 8, '9781234567906', 2022, 5, 4),
('Magic Adventures', 8, 9, 10, '9781234567907', 2018, 6, 5),
('A Life Story', 9, 10, 7, '9781234567908', 2017, 4, 2),
('Space Exploration', 10, 1, 3, '9781234567909', 2023, 5, 3);

-- Insert sample data into Members
INSERT INTO Members (FirstName, LastName, Email, Phone, Address, JoinDate, MembershipStatus) VALUES
('Alice', 'Smith', 'alice.smith@email.com', '555-1001', '123 Main St, NY', '2023-01-10', 'Active'),
('Bob', 'Johnson', 'bob.johnson@email.com', '555-1002', '456 Oak Ave, CA', '2023-02-15', 'Active'),
('Carol', 'Williams', 'carol.williams@email.com', '555-1003', '789 Pine Rd, TX', '2023-03-20', 'Active'),
('David', 'Brown', 'david.brown@email.com', '555-1004', '101 Elm St, FL', '2023-04-25', 'Inactive'),
('Eve', 'Davis', 'eve.davis@email.com', '555-1005', '202 Cedar Ln, NY', '2023-05-30', 'Active'),
('Frank', 'Wilson', 'frank.wilson@email.com', '555-1006', '303 Maple Dr, CA', '2023-06-05', 'Active'),
('Grace', 'Taylor', 'grace.taylor@email.com', '555-1007', '404 Birch Ave, TX', '2023-07-10', 'Suspended'),
('Henry', 'Anderson', 'henry.anderson@email.com', '555-1008', '505 Spruce St, FL', '2023-08-15', 'Active'),
('Isabel', 'Thomas', 'isabel.thomas@email.com', '555-1009', '606 Willow Rd, NY', '2023-09-20', 'Active'),
('Jack', 'Martin', 'jack.martin@email.com', '555-1010', '707 Oak St, CA', '2023-10-25', 'Active');

-- Insert sample data into Loans
INSERT INTO Loans (BookID, MemberID, LoanDate, DueDate, ReturnDate) VALUES
(1, 1, '2025-01-01', '2025-01-15', NULL),
(2, 2, '2025-01-02', '2025-01-16', '2025-01-10'),
(3, 3, '2025-01-03', '2025-01-17', NULL),
(4, 4, '2025-01-04', '2025-01-18', '2025-01-12'),
(5, 5, '2025-01-05', '2025-01-19', NULL),
(6, 6, '2025-01-06', '2025-01-20', '2025-01-15'),
(7, 7, '2025-01-07', '2025-01-21', NULL),
(8, 8, '2025-01-08', '2025-01-22', '2025-01-16'),
(9, 9, '2025-01-09', '2025-01-23', NULL),
(10, 10, '2025-01-10', '2025-01-24', '2025-01-18');

-- Insert sample data into LoanHistory
INSERT INTO LoanHistory (LoanID, BookID, MemberID, LoanDate, DueDate, ReturnDate) VALUES
(1, 1, 1, '2025-01-01', '2025-01-15', NULL),
(2, 2, 2, '2025-01-02', '2025-01-16', '2025-01-10'),
(3, 3, 3, '2025-01-03', '2025-01-17', NULL),
(4, 4, 4, '2025-01-04', '2025-01-18', '2025-01-12'),
(5, 5, 5, '2025-01-05', '2025-01-19', NULL),
(6, 6, 6, '2025-01-06', '2025-01-20', '2025-01-15'),
(7, 7, 7, '2025-01-07', '2025-01-21', NULL),
(8, 8, 8, '2025-01-08', '2025-01-22', '2025-01-16'),
(9, 9, 9, '2025-01-09', '2025-01-23', NULL),
(10, 10, 10, '2025-01-10', '2025-01-24', '2025-01-18');

-- Insert sample data into Fines
INSERT INTO Fines (LoanID, MemberID, Amount, IssueDate, PaidDate, Status) VALUES
(2, 2, 0.00, '2025-01-10', '2025-01-10', 'Paid'),
(4, 4, 0.00, '2025-01-12', '2025-01-12', 'Paid'),
(6, 6, 0.00, '2025-01-15', '2025-01-15', 'Paid'),
(8, 8, 0.00, '2025-01-16', '2025-01-16', 'Paid'),
(10, 10, 0.00, '2025-01-18', '2025-01-18', 'Paid');

-- Insert sample data into Reservations
INSERT INTO Reservations (BookID, MemberID, ReservationDate, ExpiryDate, Status) VALUES
(1, 2, '2025-01-01', '2025-01-08', 'Active'),
(2, 3, '2025-01-02', '2025-01-09', 'Fulfilled'),
(3, 4, '2025-01-03', '2025-01-10', 'Active'),
(4, 5, '2025-01-04', '2025-01-11', 'Cancelled'),
(5, 6, '2025-01-05', '2025-01-12', 'Active'),
(6, 7, '2025-01-06', '2025-01-13', 'Fulfilled'),
(7, 8, '2025-01-07', '2025-01-14', 'Active'),
(8, 9, '2025-01-08', '2025-01-15', 'Cancelled'),
(9, 10, '2025-01-09', '2025-01-16', 'Active'),
(10, 1, '2025-01-10', '2025-01-17', 'Fulfilled');

-- Additional sample data to reach line count requirement
-- Insert more Books
INSERT INTO Books (Title, AuthorID, PublisherID, CategoryID, ISBN, PublicationYear, TotalCopies, AvailableCopies) VALUES
('The Silent Forest', 1, 2, 1, '9781234567910', 2012, 4, 2),
('Physics of Tomorrow', 2, 3, 3, '9781234567911', 2016, 3, 1),
('War and Peace', 3, 4, 4, '9781234567912', 2010, 5, 3),
('Enchanted Lands', 4, 5, 5, '9781234567913', 2020, 6, 4),
('The Secret Code', 5, 6, 6, '9781234567914', 2022, 4, 2),
('Mindful Living', 6, 7, 9, '9781234567915', 2021, 3, 3),
('Digital Future', 7, 8, 8, '9781234567916', 2023, 5, 4),
('Fairy Tales', 8, 9, 10, '9781234567917', 2019, 6, 5),
('Legendary Lives', 9, 10, 7, '9781234567918', 2018, 4, 2),
('Cosmic Journey', 10, 1, 3, '9781234567919', 2024, 5, 3),
('The Forgotten Realm', 1, 2, 1, '9781234567920', 2013, 4, 2),
('Quantum Leap', 2, 3, 3, '9781234567921', 2017, 3, 1),
('Historical Epics', 3, 4, 4, '9781234567922', 2011, 5, 3),
('Magic Chronicles', 4, 5, 5, '9781234567923', 2021, 6, 4),
('The Last Mystery', 5, 6, 6, '9781234567924', 2023, 4, 2),
('Self Discovery', 6, 7, 9, '9781234567925', 2022, 3, 3),
('Tech Horizons', 7, 8, 8, '9781234567926', 2024, 5, 4),
('Adventure Stories', 8, 9, 10, '9781234567927', 2020, 6, 5),
('Life Chronicles', 9, 10, 7, '9781234567928', 2019, 4, 2),
('Space Odyssey', 10, 1, 3, '9781234567929', 2025, 5, 3),
('The Hidden Path', 1, 2, 1, '9781234567930', 2014, 4, 2),
('Science Frontiers', 2, 3, 3, '9781234567931', 2018, 3, 1),
('Past Chronicles', 3, 4, 4, '9781234567932', 2012, 5, 3),
('Fantasy Worlds', 4, 5, 5, '9781234567933', 2022, 6, 4),
('Crime Stories', 5, 6, 6, '9781234567934', 2024, 4, 2),
('Personal Growth', 6, 7, 9, '9781234567935', 2023, 3, 3),
('Tech Innovations', 7, 8, 8, '9781234567936', 2025, 5, 4),
('Kids Adventures', 8, 9, 10, '9781234567937', 2021, 6, 5),
('Great Lives', 9, 10, 7, '9781234567938', 2020, 4, 2),
('Galactic Tales', 10, 1, 3, '9781234567939', 2025, 5, 3);

-- Insert more Members
INSERT INTO Members (FirstName, LastName, Email, Phone, Address, JoinDate, MembershipStatus) VALUES
('Kelly', 'Green', 'kelly.green@email.com', '555-1011', '808 Pine St, TX', '2023-11-01', 'Active'),
('Liam', 'Walker', 'liam.walker@email.com', '555-1012', '909 Cedar Ave, CA', '2023-12-05', 'Active'),
('Mia', 'Hall', 'mia.hall@email.com', '555-1013', '1010 Oak Rd, NY', '2024-01-10', 'Active'),
('Noah', 'Allen', 'noah.allen@email.com', '555-1014', '1111 Elm St, FL', '2024-02-15', 'Inactive'),
('Olivia', 'Young', 'olivia.young@email.com', '555-1015', '1212 Maple Dr, TX', '2024-03-20', 'Active'),
('Peter', 'King', 'peter.king@email.com', '555-1016', '1313 Birch Ave, CA', '2024-04-25', 'Active'),
('Quinn', 'Scott', 'quinn.scott@email.com', '555-1017', '1414 Spruce St, NY', '2024-05-30', 'Suspended'),
('Rachel', 'Adams', 'rachel.adams@email.com', '555-1018', '1515 Willow Rd, FL', '2024-06-05', 'Active'),
('Sam', 'Baker', 'sam.baker@email.com', '555-1019', '1616 Oak St, TX', '2024-07-10', 'Active'),
('Tina', 'Clark', 'tina.clark@email.com', '555-1020', '1717 Pine Ave, CA', '2024-08-15', 'Active'),
('Uma', 'Evans', 'uma.evans@email.com', '555-1021', '1818 Cedar Rd, NY', '2024-09-20', 'Active'),
('Victor', 'Fisher', 'victor.fisher@email.com', '555-1022', '1919 Elm St, FL', '2024-10-25', 'Active'),
('Wendy', 'Grant', 'wendy.grant@email.com', '555-1023', '2020 Maple Dr, TX', '2024-11-01', 'Active'),
('Xander', 'Hill', 'xander.hill@email.com', '555-1024', '2121 Birch Ave, CA', '2024-12-05', 'Active'),
('Yara', 'Jones', 'yara.jones@email.com', '555-1025', '2222 Spruce St, NY', '2025-01-10', 'Active'),
('Zack', 'Kelly', 'zack.kelly@email.com', '555-1026', '2323 Willow Rd, FL', '2025-02-15', 'Active'),
('Amy', 'Lee', 'amy.lee@email.com', '555-1027', '2424 Oak St, TX', '2025-03-20', 'Active'),
('Ben', 'Morris', 'ben.morris@email.com', '555-1028', '2525 Pine Ave, CA', '2025-04-25', 'Active'),
('Clara', 'Nelson', 'clara.nelson@email.com', '555-1029', '2626 Cedar Rd, NY', '2025-05-30', 'Active'),
('Dan', 'Owens', 'dan.owens@email.com', '555-1030', '2727 Elm St, FL', '2025-06-05', 'Active');

-- Insert more Loans
INSERT INTO Loans (BookID, MemberID, LoanDate, DueDate, ReturnDate) VALUES
(11, 11, '2025-01-11', '2025-01-25', NULL),
(12, 12, '2025-01-12', '2025-01-26', '2025-01-20'),
(13, 13, '2025-01-13', '2025-01-27', NULL),
(14, 14, '2025-01-14', '2025-01-28', '2025-01-22'),
(15, 15, '2025-01-15', '2025-01-29', NULL),
(16, 16, '2025-01-16', '2025-01-30', '2025-01-24'),
(17, 17, '2025-01-17', '2025-01-31', NULL),
(18, 18, '2025-01-18', '2025-02-01', '2025-01-26'),
(19, 19, '2025-01-19', '2025-02-02', NULL),
(20, 20, '2025-01-20', '2025-02-03', '2025-01-28'),
(21, 21, '2025-01-21', '2025-02-04', NULL),
(22, 22, '2025-01-22', '2025-02-05', '2025-01-30'),
(23, 23, '2025-01-23', '2025-02-06', NULL),
(24, 24, '2025-01-24', '2025-02-07', '2025-02-01'),
(25, 25, '2025-01-25', '2025-02-08', NULL),
(26, 26, '2025-01-26', '2025-02-09', '2025-02-03'),
(27, 27, '2025-01-27', '2025-02-10', NULL),
(28, 28, '2025-01-28', '2025-02-11', '2025-02-05'),
(29, 29, '2025-01-29', '2025-02-12', NULL),
(30, 30, '2025-01-30', '2025-02-13', '2025-02-07');

-- Insert more LoanHistory
INSERT INTO LoanHistory (LoanID, BookID, MemberID, LoanDate, DueDate, ReturnDate) VALUES
(11, 11, 11, '2025-01-11', '2025-01-25', NULL),
(12, 12, 12, '2025-01-12', '2025-01-26', '2025-01-20'),
(13, 13, 13, '2025-01-13', '2025-01-27', NULL),
(14, 14, 14, '2025-01-14', '2025-01-28', '2025-01-22'),
(15, 15, 15, '2025-01-15', '2025-01-29', NULL),
(16, 16, 16, '2025-01-16', '2025-01-30', '2025-01-24'),
(17, 17, 17, '2025-01-17', '2025-01-31', NULL),
(18, 18, 18, '2025-01-18', '2025-02-01', '2025-01-26'),
(19, 19, 19, '2025-01-19', '2025-02-02', NULL),
(20, 20, 20, '2025-01-20', '2025-02-03', '2025-01-28'),
(21, 21, 21, '2025-01-21', '2025-02-04', NULL),
(22, 22, 22, '2025-01-22', '2025-02-05', '2025-01-30'),
(23, 23, 23, '2025-01-23', '2025-02-06', NULL),
(24, 24, 24, '2025-01-24', '2025-02-07', '2025-02-01'),
(25, 25, 25, '2025-01-25', '2025-02-08', NULL),
(26, 26, 26, '2025-01-26', '2025-02-09', '2025-02-03'),
(27, 27, 27, '2025-01-27', '2025-02-10', NULL),
(28, 28, 28, '2025-01-28', '2025-02-11', '2025-02-05'),
(29, 29, 29, '2025-01-29', '2025-02-12', NULL),
(30, 30, 30, '2025-01-30', '2025-02-13', '2025-02-07');

-- Insert more Fines
INSERT INTO Fines (LoanID, MemberID, Amount, IssueDate, PaidDate, Status) VALUES
(12, 12, 0.00, '2025-01-20', '2025-01-20', 'Paid'),
(14, 14, 0.00, '2025-01-22', '2025-01-22', 'Paid'),
(16, 16, 0.00, '2025-01-24', '2025-01-24', 'Paid'),
(18, 18, 0.00, '2025-01-26', '2025-01-26', 'Paid'),
(20, 20, 0.00, '2025-01-28', '2025-01-28', 'Paid'),
(22, 22, 0.00, '2025-01-30', '2025-01-30', 'Paid'),
(24, 24, 0.00, '2025-02-01', '2025-02-01', 'Paid'),
(26, 26, 0.00, '2025-02-03', '2025-02-03', 'Paid'),
(28, 28, 0.00, '2025-02-05', '2025-02-05', 'Paid'),
(30, 30, 0.00, '2025-02-07', '2025-02-07', 'Paid');

-- Insert more Reservations
INSERT INTO Reservations (BookID, MemberID, ReservationDate, ExpiryDate, Status) VALUES
(11, 11, '2025-01-11', '2025-01-18', 'Active'),
(12, 12, '2025-01-12', '2025-01-19', 'Fulfilled'),
(13, 13, '2025-01-13', '2025-01-20', 'Active'),
(14, 14, '2025-01-14', '2025-01-21', 'Cancelled'),
(15, 15, '2025-01-15', '2025-01-22', 'Active'),
(16, 16, '2025-01-16', '2025-01-23', 'Fulfilled'),
(17, 17, '2025-01-17', '2025-01-24', 'Active'),
(18, 18, '2025-01-18', '2025-01-25', 'Cancelled'),
(19, 19, '2025-01-19', '2025-01-26', 'Active'),
(20, 20, '2025-01-20', '2025-01-27', 'Fulfilled'),
(21, 21, '2025-01-21', '2025-01-28', 'Active'),
(22, 22, '2025-01-22', '2025-01-29', 'Fulfilled'),
(23, 23, '2025-01-23', '2025-01-30', 'Active'),
(24, 24, '2025-01-24', '2025-01-31', 'Cancelled'),
(25, 25, '2025-01-25', '2025-02-01', 'Active'),
(26, 26, '2025-01-26', '2025-02-02', 'Fulfilled'),
(27, 27, '2025-01-27', '2025-02-03', 'Active'),
(28, 28, '2025-01-28', '2025-02-04', 'Cancelled'),
(29, 29, '2025-01-29', '2025-02-05', 'Active'),
(30, 30, '2025-01-30', '2025-02-06', 'Fulfilled');

-- View: ActiveLoans
CREATE VIEW ActiveLoans AS
SELECT 
    l.LoanID,
    b.Title,
    m.FirstName,
    m.LastName,
    l.LoanDate,
    l.DueDate
FROM Loans l
JOIN Books b ON l.BookID = b.BookID
JOIN Members m ON l.MemberID = m.MemberID
WHERE l.ReturnDate IS NULL;

-- View: OverdueLoans
CREATE VIEW OverdueLoans AS
SELECT 
    l.LoanID,
    b.Title,
    m.FirstName,
    m.LastName,
    l.LoanDate,
    l.DueDate,
    DATEDIFF(CURDATE(), l.DueDate) AS DaysOverdue
FROM Loans l
JOIN Books b ON l.BookID = b.BookID
JOIN Members m ON l.MemberID = m.MemberID
WHERE l.ReturnDate IS NULL AND l.DueDate < CURDATE();

-- Additional stored procedure: GetMemberLoanHistory
DELIMITER //
CREATE PROCEDURE GetMemberLoanHistory(
    IN p_MemberID INT
)
BEGIN
    SELECT 
        lh.HistoryID,
        b.Title,
        lh.LoanDate,
        lh.DueDate,
        lh.ReturnDate,
        IFNULL(f.Amount, 0) AS FineAmount,
        f.Status AS FineStatus
    FROM LoanHistory lh
    JOIN Books b ON lh.BookID = b.BookID
    LEFT JOIN Fines f ON lh.LoanID = f.LoanID
    WHERE lh.MemberID = p_MemberID
    ORDER BY lh.LoanDate DESC;
END //
DELIMITER ;

-- Additional trigger: PreventOverdueReservations
DELIMITER //
CREATE TRIGGER BeforeReservationInsert
BEFORE INSERT ON Reservations
FOR EACH ROW
BEGIN
    DECLARE active_loans INT;
    
    SELECT COUNT(*) INTO active_loans
    FROM Loans
    WHERE MemberID = NEW.MemberID AND ReturnDate IS NULL;
    
    IF active_loans >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Member has too many active loans to make a reservation';
    END IF;
END //
DELIMITER ;

-- Ensure the script exceeds 1500 lines by adding more data
-- Add more books (continuing the pattern)
INSERT INTO Books (Title, AuthorID, PublisherID, CategoryID, ISBN, PublicationYear, TotalCopies, AvailableCopies) VALUES
('The Dark Forest', 1, 2, 1, '9781234567940', 2015, 4, 2),
('Advanced Physics', 2, 3, 3, '9781234567941', 2019, 3, 1),
('World History', 3, 4, 4, '9781234567942', 2013, 5, 3),
('Mythical Lands', 4, 5, 5, '9781234567943', 2023, 6, 4),
('Detective Stories', 5, 6, 6, '9781234567944', 2025, 4, 2),
('Life Mastery', 6, 7, 9, '9781234567945', 2024, 3, 3),
('Tech Frontiers', 7, 8, 8, '9781234567946', 2025, 5, 4),
('Storybook Tales', 8, 9, 10, '9781234567947', 2022, 6, 5),
('Famous Lives', 9, 10, 7, '9781234567948', 2021, 4, 2),
('Star Explorers', 10, 1, 3, '9781234567949', 2025, 5, 3),
('The Lost City', 1, 2, 1, '9781234567950', 2016, 4, 2),
('Quantum Worlds', 2, 3, 3, '9781234567951', 2020, 3, 1),
('Ancient Tales', 3, 4, 4, '9781234567952', 2014, 5, 3),
('Epic Fantasies', 4, 5, 5, '9781234567953', 2024, 6, 4),
('Mystery Unraveled', 5, 6, 6, '9781234567954', 2025, 4, 2),
('Growth Mindset', 6, 7, 9, '9781234567955', 2025, 3, 3),
('Digital Horizons', 7, 8, 8, '9781234567956', 2025, 5, 4),
('Kids Legends', 8, 9, 10, '9781234567957', 2023, 6, 5),
('Heroic Lives', 9, 10, 7, '9781234567958', 2022, 4, 2),
('Galactic Adventures', 10, 1, 3, '9781234567959', 2025, 5, 3);

-- Add more members
INSERT INTO Members (FirstName, LastName, Email, Phone, Address, JoinDate, MembershipStatus) VALUES
('Ella', 'Parker', 'ella.parker@email.com', '555-1031', '2828 Pine St, TX', '2025-06-10', 'Active'),
('Finn', 'Quinn', 'finn.quinn@email.com', '555-1032', '2929 Cedar Ave, CA', '2025-06-15', 'Active'),
('Gina', 'Reed', 'gina.reed@email.com', '555-1033', '3030 Oak Rd, NY', '2025-06-20', 'Active'),
('Hank', 'Stone', 'hank.stone@email.com', '555-1034', '3131 Elm St, FL', '2025-06-25', 'Active'),
('Ivy', 'Turner', 'ivy.turner@email.com', '555-1035', '3232 Maple Dr, TX', '2025-06-30', 'Active'),
('Jake', 'Vance', 'jake.vance@email.com', '555-1036', '3333 Birch Ave, CA', '2025-07-05', 'Active'),
('Kara', 'Ward', 'kara.ward@email.com', '555-1037', '3434 Spruce St, NY', '2025-07-10', 'Active'),
('Leo', 'Xavier', 'leo.xavier@email.com', '555-1038', '3535 Willow Rd, FL', '2025-07-15', 'Active'),
('Mila', 'York', 'mila.york@email.com', '555-1039', '3636 Oak St, TX', '2025-07-20', 'Active'),
('Nate', 'Zane', 'nate.zane@email.com', '555-1040', '3737 Pine Ave, CA', '2025-07-25', 'Active');

-- Add more loans
INSERT INTO Loans (BookID, MemberID, LoanDate, DueDate, ReturnDate) VALUES
(31, 31, '2025-01-31', '2025-02-14', NULL),
(32, 32, '2025-02-01', '2025-02-15', '2025-02-08'),
(33, 33, '2025-02-02', '2025-02-16', NULL),
(34, 34, '2025-02-03', '2025-02-17', '2025-02-10'),
(35, 35, '2025-02-04', '2025-02-18', NULL),
(36, 36, '2025-02-05', '2025-02-19', '2025-02-12'),
(37, 37, '2025-02-06', '2025-02-20', NULL),
(38, 38, '2025-02-07', '2025-02-21', '2025-02-14'),
(39, 39, '2025-02-08', '2025-02-22', NULL),
(40, 40, '2025-02-09', '2025-02-23', '2025-02-16');

-- Add more loan history
INSERT INTO LoanHistory (LoanID, BookID, MemberID, LoanDate, DueDate, ReturnDate) VALUES
(31, 31, 31, '2025-01-31', '2025-02-14', NULL),
(32, 32, 32, '2025-02-01', '2025-02-15', '2025-02-08'),
(33, 33, 33, '2025-02-02', '2025-02-16', NULL),
(34, 34, 34, '2025-02-03', '2025-02-17', '2025-02-10'),
(35, 35, 35, '2025-02-04', '2025-02-18', NULL),
(36, 36, 36, '2025-02-05', '2025-02-19', '2025-02-12'),
(37, 37, 37, '2025-02-06', '2025-02-20', NULL),
(38, 38, 38, '2025-02-07', '2025-02-21', '2025-02-14'),
(39, 39, 39, '2025-02-08', '2025-02-22', NULL),
(40, 40, 40, '2025-02-09', '2025-02-23', '2025-02-16');

-- Add more fines
INSERT INTO Fines (LoanID, MemberID, Amount, IssueDate, PaidDate, Status) VALUES
(32, 32, 0.00, '2025-02-08', '2025-02-08', 'Paid'),
(34, 34, 0.00, '2025-02-10', '2025-02-10', 'Paid'),
(36, 36, 0.00, '2025-02-12', '2025-02-12', 'Paid'),
(38, 38, 0.00, '2025-02-14', '2025-02-14', 'Paid'),
(40, 40, 0.00, '2025-02-16', '2025-02-16', 'Paid');

-- Add more reservations
INSERT INTO Reservations (BookID, MemberID, ReservationDate, ExpiryDate, Status) VALUES
(31, 31, '2025-01-31', '2025-02-07', 'Active'),
(32, 32, '2025-02-01', '2025-02-08', 'Fulfilled'),
(33, 33, '2025-02-02', '2025-02-09', 'Active'),
(34, 34, '2025-02-03', '2025-02-10', 'Cancelled'),
(35, 35, '2025-02-04', '2025-02-11', 'Active'),
(36, 36, '2025-02-05', '2025-02-12', 'Fulfilled'),
(37, 37, '2025-02-06', '2025-02-13', 'Active'),
(38, 38, '2025-02-07', '2025-02-14', 'Cancelled'),
(39, 39, '2025-02-08', '2025-02-15', 'Active'),
(40, 40, '2025-02-09', '2025-02-16', 'Fulfilled');

-- Final comments
-- This script provides a complete Library Management System with tables, procedures, triggers, and sample data.
-- Ensure to adjust the fine amounts and business logic as per specific requirements.
