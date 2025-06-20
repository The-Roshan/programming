import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.UUID;

// Class to represent a Book
class Book {
    private String bookId;
    private String title;
    private String author;
    private String isbn;
    private int publicationYear;
    private String category;
    private int totalCopies;
    private int availableCopies;

    public Book(String title, String author, String isbn, int publicationYear, String category, int totalCopies) {
        this.bookId = UUID.randomUUID().toString();
        this.title = title;
        this.author = author;
        this.isbn = isbn;
        this.publicationYear = publicationYear;
        this.category = category;
        this.totalCopies = totalCopies;
        this.availableCopies = totalCopies;
    }

    // Getters and Setters
    public String getBookId() { return bookId; }
    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public String getIsbn() { return isbn; }
    public int getPublicationYear() { return publicationYear; }
    public String getCategory() { return category; }
    public int getTotalCopies() { return totalCopies; }
    public int getAvailableCopies() { return availableCopies; }

    public void setAvailableCopies(int availableCopies) {
        if (availableCopies >= 0 && availableCopies <= totalCopies) {
            this.availableCopies = availableCopies;
        } else {
            throw new IllegalArgumentException("Invalid number of available copies");
        }
    }

    @Override
    public String toString() {
        return "Book{" +
                "bookId='" + bookId + '\'' +
                ", title='" + title + '\'' +
                ", author='" + author + '\'' +
                ", isbn='" + isbn + '\'' +
                ", publicationYear=" + publicationYear +
                ", category='" + category + '\'' +
                ", totalCopies=" + totalCopies +
                ", availableCopies=" + availableCopies +
                '}';
    }
}

// Class to represent a Member
class Member {
    private String memberId;
    private String firstName;
    private String lastName;
    private String email;
    private String phone;
    private String address;
    private LocalDate joinDate;
    private String status;

    public Member(String firstName, String lastName, String email, String phone, String address) {
        this.memberId = UUID.randomUUID().toString();
        this.firstName = firstName;
        this.lastName = lastName;
        this.email = email;
        this.phone = phone;
        this.address = address;
        this.joinDate = LocalDate.now();
        this.status = "Active";
    }

    // Getters and Setters
    public String getMemberId() { return memberId; }
    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public String getEmail() { return email; }
    public String getPhone() { return phone; }
    public String getAddress() { return address; }
    public LocalDate getJoinDate() { return joinDate; }
    public String getStatus() { return status; }
    public void setStatus(String status) {
        if (status.equals("Active") || status.equals("Inactive") || status.equals("Suspended")) {
            this.status = status;
        } else {
            throw new IllegalArgumentException("Invalid status");
        }
    }

    @Override
    public String toString() {
        return "Member{" +
                "memberId='" + memberId + '\'' +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", email='" + email + '\'' +
                ", phone='" + phone + '\'' +
                ", address='" + address + '\'' +
                ", joinDate=" + joinDate +
                ", status='" + status + '\'' +
                '}';
    }
}

// Class to represent a Loan
class Loan {
    private String loanId;
    private String bookId;
    private String memberId;
    private LocalDate loanDate;
    private LocalDate dueDate;
    private LocalDate returnDate;

    public Loan(String bookId, String memberId, LocalDate loanDate, LocalDate dueDate) {
        this.loanId = UUID.randomUUID().toString();
        this.bookId = bookId;
        this.memberId = memberId;
        this.loanDate = loanDate;
        this.dueDate = dueDate;
        this.returnDate = null;
    }

    // Getters and Setters
    public String getLoanId() { return loanId; }
    public String getBookId() { return bookId; }
    public String getMemberId() { return memberId; }
    public LocalDate getLoanDate() { return loanDate; }
    public LocalDate getDueDate() { return dueDate; }
    public LocalDate getReturnDate() { return returnDate; }
    public void setReturnDate(LocalDate returnDate) { this.returnDate = returnDate; }

    public double calculateFine() {
        if (returnDate != null && returnDate.isAfter(dueDate)) {
            long daysOverdue = ChronoUnit.DAYS.between(dueDate, returnDate);
            return daysOverdue * 1.00; // $1 per day overdue
        }
        return 0.0;
    }

    @Override
    public String toString() {
        return "Loan{" +
                "loanId='" + loanId + '\'' +
                ", bookId='" + bookId + '\'' +
                ", memberId='" + memberId + '\'' +
                ", loanDate=" + loanDate +
                ", dueDate=" + dueDate +
                ", returnDate=" + returnDate +
                '}';
    }
}

// Class to represent a Reservation
class Reservation {
    private String reservationId;
    private String bookId;
    private String memberId;
    private LocalDate reservationDate;
    private LocalDate expiryDate;
    private String status;

    public Reservation(String bookId, String memberId, LocalDate reservationDate, LocalDate expiryDate) {
        this.reservationId = UUID.randomUUID().toString();
        this.bookId = bookId;
        this.memberId = memberId;
        this.reservationDate = reservationDate;
        this.expiryDate = expiryDate;
        this.status = "Active";
    }

    // Getters and Setters
    public String getReservationId() { return reservationId; }
    public String getBookId() { return bookId; }
    public String getMemberId() { return memberId; }
    public LocalDate getReservationDate() { return reservationDate; }
    public LocalDate getExpiryDate() { return expiryDate; }
    public String getStatus() { return status; }
    public void setStatus(String status) {
        if (status.equals("Active") || status.equals("Fulfilled") || status.equals("Cancelled")) {
            this.status = status;
        } else {
            throw new IllegalArgumentException("Invalid reservation status");
        }
    }

    @Override
    public String toString() {
        return "Reservation{" +
                "reservationId='" + reservationId + '\'' +
                ", bookId='" + bookId + '\'' +
                ", memberId='" + memberId + '\'' +
                ", reservationDate=" + reservationDate +
                ", expiryDate=" + expiryDate +
                ", status='" + status + '\'' +
                '}';
    }
}

// Main Library Management System class
public class LibraryManagementSystem {
    private Map<String, Book> books;
    private Map<String, Member> members;
    private List<Loan> loans;
    private List<Reservation> reservations;
    private Scanner scanner;

    public LibraryManagementSystem() {
        books = new HashMap<>();
        members = new HashMap<>();
        loans = new ArrayList<>();
        reservations = new ArrayList<>();
        scanner = new Scanner(System.in);
    }

    // Add a new book
    public void addBook(String title, String author, String isbn, int publicationYear, String category, int totalCopies) {
        Book book = new Book(title, author, isbn, publicationYear, category, totalCopies);
        books.put(book.getBookId(), book);
        System.out.println("Book added: " + book.getTitle());
    }

    // Add a new member
    public void addMember(String firstName, String lastName, String email, String phone, String address) {
        Member member = new Member(firstName, lastName, email, phone, address);
        members.put(member.getMemberId(), member);
        System.out.println("Member added: " + member.getFirstName() + " " + member.getLastName());
    }

    // Borrow a book
    public void borrowBook(String bookId, String memberId) {
        Book book = books.get(bookId);
        Member member = members.get(memberId);

        if (book == null) {
            System.out.println("Book not found.");
            return;
        }
        if (member == null) {
            System.out.println("Member not found.");
            return;
        }
        if (!member.getStatus().equals("Active")) {
            System.out.println("Member is not active and cannot borrow books.");
            return;
        }
        if (book.getAvailableCopies() <= 0) {
            System.out.println("No copies available for borrowing.");
            return;
        }

        LocalDate loanDate = LocalDate.now();
        LocalDate dueDate = loanDate.plusWeeks(2);
        Loan loan = new Loan(bookId, memberId, loanDate, dueDate);
        loans.add(loan);
        book.setAvailableCopies(book.getAvailableCopies() - 1);
        System.out.println("Book borrowed: " + book.getTitle() + " by " + member.getFirstName() + " " + member.getLastName());
    }

    // Return a book
    public void returnBook(String loanId, LocalDate returnDate) {
        Loan loan = loans.stream()
                .filter(l -> l.getLoanId().equals(loanId))
                .findFirst()
                .orElse(null);

        if (loan == null) {
            System.out.println("Loan not found.");
            return;
        }

        Book book = books.get(loan.getBookId());
        if (book == null) {
            System.out.println("Book not found.");
            return;
        }

        loan.setReturnDate(returnDate);
        book.setAvailableCopies(book.getAvailableCopies() + 1);
        double fine = loan.calculateFine();
        if (fine > 0) {
            System.out.println("Fine incurred: $" + fine);
        }
        System.out.println("Book returned: " + book.getTitle());
    }

    // Reserve a book
    public void reserveBook(String bookId, String memberId) {
        Book book = books.get(bookId);
        Member member = members.get(memberId);

        if (book == null) {
            System.out.println("Book not found.");
            return;
        }
        if (member == null) {
            System.out.println("Member not found.");
            return;
        }
        if (!member.getStatus().equals("Active")) {
            System.out.println("Member is not active and cannot reserve books.");
            return;
        }

        long activeLoans = loans.stream()
                .filter(l -> l.getMemberId().equals(memberId) && l.getReturnDate() == null)
                .count();
        if (activeLoans >= 3) {
            System.out.println("Member has too many active loans to reserve a book.");
            return;
        }

        LocalDate reservationDate = LocalDate.now();
        LocalDate expiryDate = reservationDate.plusDays(7);
        Reservation reservation = new Reservation(bookId, memberId, reservationDate, expiryDate);
        reservations.add(reservation);
        System.out.println("Book reserved: " + book.getTitle() + " for " + member.getFirstName() + " " + member.getLastName());
    }

    // List all books
    public void listBooks() {
        if (books.isEmpty()) {
            System.out.println("No books available.");
            return;
        }
        books.values().forEach(System.out::println);
    }

    // List all members
    public void listMembers() {
        if (members.isEmpty()) {
            System.out.println("No members registered.");
            return;
        }
        members.values().forEach(System.out::println);
    }

    // List active loans
    public void listActiveLoans() {
        List<Loan> activeLoans = loans.stream()
                .filter(loan -> loan.getReturnDate() == null)
                .toList();
        if (activeLoans.isEmpty()) {
            System.out.println("No active loans.");
            return;
        }
        activeLoans.forEach(loan -> {
            Book book = books.get(loan.getBookId());
            Member member = members.get(loan.getMemberId());
            System.out.println("Loan ID: " + loan.getLoanId() +
                    ", Book: " + (book != null ? book.getTitle() : "Unknown") +
                    ", Member: " + (member != null ? member.getFirstName() + " " + member.getLastName() : "Unknown") +
                    ", Due Date: " + loan.getDueDate());
        });
    }

    // List overdue loans
    public void listOverdueLoans() {
        LocalDate today = LocalDate.now();
        List<Loan> overdueLoans = loans.stream()
                .filter(loan -> loan.getReturnDate() == null && loan.getDueDate().isBefore(today))
                .toList();
        if (overdueLoans.isEmpty()) {
            System.out.println("No overdue loans.");
            return;
        }
        overdueLoans.forEach(loan -> {
            Book book = books.get(loan.getBookId());
            Member member = members.get(loan.getMemberId());
            long daysOverdue = ChronoUnit.DAYS.between(loan.getDueDate(), today);
            System.out.println("Loan ID: " + loan.getLoanId() +
                    ", Book: " + (book != null ? book.getTitle() : "Unknown") +
                    ", Member: " + (member != null ? member.getFirstName() + " " + member.getLastName() : "Unknown") +
                    ", Days Overdue: " + daysOverdue);
        });
    }

    // Console-based menu
    public void start() {
        while (true) {
            System.out.println("\n=== Library Management System ===");
            System.out.println("1. Add Book");
            System.out.println("2. Add Member");
            System.out.println("3. Borrow Book");
            System.out.println("4. Return Book");
            System.out.println("5. Reserve Book");
            System.out.println("6. List All Books");
            System.out.println("7. List All Members");
            System.out.println("8. List Active Loans");
            System.out.println("9. List Overdue Loans");
            System.out.println("10. Exit");
            System.out.print("Choose an option: ");

            int choice;
            try {
                choice = Integer.parseInt(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a number.");
                continue;
            }

            switch (choice) {
                case 1:
                    System.out.print("Enter book title: ");
                    String title = scanner.nextLine();
                    System.out.print("Enter author: ");
                    String author = scanner.nextLine();
                    System.out.print("Enter ISBN: ");
                    String isbn = scanner.nextLine();
                    System.out.print("Enter publication year: ");
                    int year;
                    try {
                        year = Integer.parseInt(scanner.nextLine());
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid year. Using default 2023.");
                        year = 2023;
                    }
                    System.out.print("Enter category: ");
                    String category = scanner.nextLine();
                    System.out.print("Enter total copies: ");
                    int copies;
                    try {
                        copies = Integer.parseInt(scanner.nextLine());
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid number. Using default 1.");
                        copies = 1;
                    }
                    addBook(title, author, isbn, year, category, copies);
                    break;

                case 2:
                    System.out.print("Enter first name: ");
                    String firstName = scanner.nextLine();
                    System.out.print("Enter last name: ");
                    String lastName = scanner.nextLine();
                    System.out.print("Enter email: ");
                    String email = scanner.nextLine();
                    System.out.print("Enter phone: ");
                    String phone = scanner.nextLine();
                    System.out.print("Enter address: ");
                    String address = scanner.nextLine();
                    addMember(firstName, lastName, email, phone, address);
                    break;

                case 3:
                    System.out.print("Enter book ID: ");
                    String bookId = scanner.nextLine();
                    System.out.print("Enter member ID: ");
                    String memberId = scanner.nextLine();
                    borrowBook(bookId, memberId);
                    break;

                case 4:
                    System.out.print("Enter loan ID: ");
                    String loanId = scanner.nextLine();
                    System.out.print("Enter return date (YYYY-MM-DD): ");
                    LocalDate returnDate;
                    try {
                        returnDate = LocalDate.parse(scanner.nextLine());
                    } catch (Exception e) {
                        System.out.println("Invalid date. Using today’s date.");
                        returnDate = LocalDate.now();
                    }
                    returnBook(loanId, returnDate);
                    break;

                case 5:
                    System.out.print("Enter book ID: ");
                    String reserveBookId = scanner.nextLine();
                    System.out.print("Enter member ID: ");
                    String reserveMemberId = scanner.nextLine();
                    reserveBook(reserveBookId, reserveMemberId);
                    break;

                case 6:
                    listBooks();
                    break;

                case 7:
                    listMembers();
                    break;

                case 8:
                    listActiveLoans();
                    break;

                case 9:
                    listOverdueLoans();
                    break;

                case 10:
                    System.out.println("Exiting system...");
                    scanner.close();
                    return;

                default:
                    System.out.println("Invalid option. Please try again.");
            }
        }
    }

    // Main method with sample data
    public static void main(String[] args) {
        LibraryManagementSystem library = new LibraryManagementSystem();

        // Add sample books
        library.addBook("The Great Adventure", "John Smith", "9781234567890", 2010, "Fiction", 5);
        library.addBook("Science Unveiled", "Emma Johnson", "9781234567891", 2015, "Science", 3);
        library.addBook("History of Time", "Michael Brown", "9781234567892", 2008, "History", 4);
        library.addBook("Mystic Realms", "Sarah Davis", "9781234567893", 2018, "Fantasy", 6);
        library.addBook("Murder Mystery", "David Wilson", "9781234567894", 2020, "Mystery", 5);
        library.addBook("Life Lessons", "Jane Taylor", "9781234567895", 2019, "Self-Help", 3);
        library.addBook("Tech Revolution", "Robert Anderson", "9781234567896", 2021, "Technology", 4);
        library.addBook("Kids Tales", "Emily White", "9781234567897", 2017, "Children", 7);
        library.addBook("Biography of a Hero", "Thomas Harris", "9781234567898", 2016, "Biography", 3);
        library.addBook("Future Visions", "Laura Martin", "9781234567899", 2022, "Science", 5);
        library.addBook("The Lost Kingdom", "John Smith", "9781234567900", 2011, "Fiction", 4);
        library.addBook("Quantum Physics", "Emma Johnson", "9781234567901", 2014, "Science", 3);
        library.addBook("Ancient Civilizations", "Michael Brown", "9781234567902", 2009, "History", 5);
        library.addBook("Dragon Tales", "Sarah Davis", "9781234567903", 2019, "Fantasy", 6);
        library.addBook("The Hidden Clue", "David Wilson", "9781234567904", 2021, "Mystery", 4);
        library.addBook("Grow Yourself", "Jane Taylor", "9781234567905", 2020, "Self-Help", 3);
        library.addBook("AI Revolution", "Robert Anderson", "9781234567906", 2022, "Technology", 5);
        library.addBook("Magic Adventures", "Emily White", "9781234567907", 2018, "Children", 6);
        library.addBook("A Life Story", "Thomas Harris", "9781234567908", 2017, "Biography", 4);
        library.addBook("Space Exploration", "Laura Martin", "9781234567909", 2023, "Science", 5);

        // Add sample members
        library.addMember("Alice", "Smith", "alice.smith@email.com", "555-1001", "123 Main St, NY");
        library.addMember("Bob", "Johnson", "bob.johnson@email.com", "555-1002", "456 Oak Ave, CA");
        library.addMember("Carol", "Williams", "carol.williams@email.com", "555-1003", "789 Pine Rd, TX");
        library.addMember("David", "Brown", "david.brown@email.com", "555-1004", "101 Elm St, FL");
        library.addMember("Eve", "Davis", "eve.davis@email.com", "555-1005", "202 Cedar Ln, NY");
        library.addMember("Frank", "Wilson", "frank.wilson@email.com", "555-1006", "303 Maple Dr, CA");
        library.addMember("Grace", "Taylor", "grace.taylor@email.com", "555-1007", "404 Birch Ave, TX");
        library.addMember("Henry", "Anderson", "henry.anderson@email.com", "555-1008", "505 Spruce St, FL");
        library.addMember("Isabel", "Thomas", "isabel.thomas@email.com", "555-1009", "606 Willow Rd, NY");
        library.addMember("Jack", "Martin", "jack.martin@email.com", "555-1010", "707 Oak St, CA");

        // Start the system
        library.start();
    }
}