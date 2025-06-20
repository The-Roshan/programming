# 📚 Library Management System Showcase

## 🌟 Overview
The **Library Management System Showcase** is a comprehensive project demonstrating a library management system implemented in **C**, **C++**, **Java**, **Python**, and **SQL**. Each implementation provides core functionalities such as managing books, members, loans, and reservations, showcasing the strengths and paradigms of each programming language. This project is designed to serve as an educational resource for developers to compare and contrast different programming approaches for the same application.

- **C**: A procedural implementation with file-based persistence and efficient memory management.
- **C++**: An object-oriented approach leveraging classes and STL for robust data handling.
- **Java**: A platform-independent, object-oriented implementation with strong type safety and collections.
- **Python**: A high-level, readable implementation with dynamic typing and list-based storage.
- **SQL**: A database-driven implementation with relational tables, stored procedures, and triggers.

This project is authored by **The-Roshan** and is intended for learning, demonstration, and further development.

## 🚀 Features
- **📖 Book Management**: Add, list, and manage book inventory (title, author, ISBN, etc.).
- **👤 Member Management**: Register and manage library members with status tracking.
- **📅 Loan Management**: Handle book borrowing, returns, and fine calculations.
- **🔒 Reservation System**: Reserve books for members with active loans limits.
- **💾 Data Persistence**:
  - C/C++: File-based storage (`.dat` files).
  - Java/Python: In-memory storage with optional file persistence.
  - SQL: Relational database with persistent storage.
- **🛠️ Error Handling**: Robust input validation and error messages across all implementations.
- **📊 Console Interface**: User-friendly menu-driven interface for all languages.

## 📂 File Structure
```
LibraryManagementShowcase/
├── c/
│   ├── library_management.c     # 📄 C implementation
│   ├── books.dat               # 💾 Book data file
│   ├── members.dat             # 💾 Member data file
│   ├── loans.dat               # 💾 Loan data file
│   ├── reservations.dat        # 💾 Reservation data file
├── cpp/
│   ├── library_management.cpp   # 📄 C++ implementation
│   ├── books.dat               # 💾 Book data file
│   ├── members.dat             # 💾 Member data file
│   ├── loans.dat               # 💾 Loan data file
│   ├── reservations.dat        # 💾 Reservation data file
├── java/
│   ├── LibraryManagementSystem.java  # 📄 Java implementation
├── python/
│   ├── library_management.py    # 📄 Python implementation
├── sql/
│   ├── library_management.sql   # 📄 SQL schema and procedures
└── README.md                   # 📖 Project documentation
```

## 🛠️ Installation
Follow the instructions below to set up and run each implementation.

### C Implementation
1. **Prerequisites**: A C compiler (e.g., GCC).
2. **Setup**:
   ```bash
   cd c
   gcc library_management.c -o library_management
   ```
3. **Run**:
   ```bash
   ./library_management
   ```

### C++ Implementation
1. **Prerequisites**: A C++ compiler (e.g., G++).
2. **Setup**:
   ```bash
   cd cpp
   g++ library_management.cpp -o library_management
   ```
3. **Run**:
   ```bash
   ./library_management
   ```

### Java Implementation
1. **Prerequisites**: Java Development Kit (JDK) 8 or higher.
2. **Setup**:
   ```bash
   cd java
   javac LibraryManagementSystem.java
   ```
3. **Run**:
   ```bash
   java LibraryManagementSystem
   ```

### Python Implementation
1. **Prerequisites**: Python 3.6 or higher.
2. **Setup**:
   ```bash
   cd python
   ```
3. **Run**:
   ```bash
   python3 library_management.py
   ```

### SQL Implementation
1. **Prerequisites**: A relational database management system (e.g., MySQL, PostgreSQL).
2. **Setup**:
   - Import the SQL script into your database:
     ```bash
     cd sql
     mysql -u <username> -p <database_name> < library_management.sql
     ```
3. **Run**:
   - Use a SQL client to execute queries or stored procedures (e.g., `CALL BorrowBook(...)`).

## 📋 Usage
Each implementation provides a console-based menu with the following options:
1. **Add Book**: Register a new book with title, author, ISBN, etc.
2. **Add Member**: Register a new library member.
3. **Borrow Book**: Issue a book to a member.
4. **Return Book**: Return a borrowed book and calculate fines if overdue.
5. **Reserve Book**: Reserve a book for a member.
6. **List Books**: Display all books in the library.
7. **List Members**: Display all registered members.
8. **List Active Loans**: Show current loans.
9. **List Overdue Loans**: Show loans past due date.
10. **Exit**: Save data and exit the program.

### Example Usage
- **C/C++**: Run the compiled executable and follow the menu prompts. Data is saved to `.dat` files.
- **Java**: Run the Java program and interact via the console. Data is stored in memory.
- **Python**: Run the Python script and use the menu. Data is stored in memory or files (if implemented).
- **SQL**: Execute stored procedures (e.g., `BorrowBook`) or queries in your SQL client.

## 🔧 Customization
- **C/C++**:
  - Modify `library_management.c/cpp` to change limits (e.g., `MAX_BOOKS`).
  - Adjust file formats in `saveLibrary` and `loadLibrary` functions.
- **Java**:
  - Extend `LibraryManagementSystem.java` to add features like file persistence or GUI.
  - Modify fine rates in the `Loan` class.
- **Python**:
  - Update `library_management.py` to include additional fields or JSON persistence.
  - Adjust loan periods or fine calculations.
- **SQL**:
  - Modify `library_management.sql` to add new tables or procedures.
  - Update fine calculations in the `ReturnBook` procedure.

## 🖥️ Dependencies
- **C/C++**: Standard libraries (`stdio.h`, `stdlib.h`, `string.h`, `time.h`).
- **Java**: Standard Java libraries (no external dependencies).
- **Python**: Standard Python libraries (no external dependencies).
- **SQL**: Compatible with MySQL, PostgreSQL, or similar RDBMS.
- **File System**: C/C++ implementations require write access for `.dat` files.

## 🌐 Browser Compatibility
Not applicable, as all implementations are console-based or database-driven.

## 🤝 Contributing
Contributions are welcome! To contribute:
1. Fork the repository: `https://github.com/The-Roshan/LibraryManagementShowcase`.
2. Create a branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

## 📜 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 📞 Contact
- **👤 Author**: The-Roshan
- **📧 Email**: [roshanjsr5555@gmail.com](mailto:roshanjsr5555@gmail.com)
- **🌐 GitHub**: [The-Roshan](https://github.com/The-Roshan)

For questions or feedback, open an issue on the GitHub repository.

## 🙏 Acknowledgments
- Inspired by classic library management systems.
- Thanks to open-source communities for providing robust tools and libraries.
