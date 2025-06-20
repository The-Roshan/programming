#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_BOOKS 100
#define MAX_MEMBERS 100
#define MAX_LOANS 200
#define MAX_RESERVATIONS 100
#define MAX_STR 100
#define LOAN_PERIOD_DAYS 14
#define FINE_PER_DAY 1.00

// Structure for Date
typedef struct {
    int day, month, year;
} Date;

// Structure for Book
typedef struct {
    char bookId[37];
    char title[MAX_STR];
    char author[MAX_STR];
    char isbn[14];
    int publicationYear;
    char category[MAX_STR];
    int totalCopies;
    int availableCopies;
} Book;

// Structure for Member
typedef struct {
    char memberId[37];
    char firstName[MAX_STR];
    char lastName[MAX_STR];
    char email[MAX_STR];
    char phone[20];
    char address[MAX_STR];
    Date joinDate;
    char status[20];
} Member;

// Structure for Loan
typedef struct {
    char loanId[37];
    char bookId[37];
    char memberId[37];
    Date loanDate;
    Date dueDate;
    Date returnDate;
    int isReturned;
} Loan;

// Structure for Reservation
typedef struct {
    char reservationId[37];
    char bookId[37];
    char memberId[37];
    Date reservationDate;
    Date expiryDate;
    char status[20];
} Reservation;

// Structure for Library
typedef struct {
    Book books[MAX_BOOKS];
    Member members[MAX_MEMBERS];
    Loan loans[MAX_LOANS];
    Reservation reservations[MAX_RESERVATIONS];
    int bookCount;
    int memberCount;
    int loanCount;
    int reservationCount;
} Library;

// Generate a simple UUID-like string
void generateUUID(char *uuid) {
    sprintf(uuid, "%ld-%d", time(NULL), rand() % 10000);
}

// Parse date from string (YYYY-MM-DD)
int parseDate(const char *dateStr, Date *date) {
    return sscanf(dateStr, "%d-%d-%d", &date->year, &date->month, &date->day) == 3;
}

// Format date to string
void formatDate(const Date *date, char *dateStr) {
    sprintf(dateStr, "%04d-%02d-%02d", date->year, date->month, date->day);
}

// Get current date
void getCurrentDate(Date *date) {
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    date->year = tm.tm_year + 1900;
    date->month = tm.tm_mon + 1;
    date->day = tm.tm_mday;
}

// Add days to date (simplified)
void addDaysToDate(Date *start, int days, Date *result) {
    *result = *start;
    result->day += days;
    while (result->day > 30) {
        result->day -= 30;
        result->month++;
        if (result->month > 12) {
            result->month = 1;
            result->year++;
        }
    }
}

// Calculate days between dates (simplified)
long daysBetweenDates(Date *start, Date *end) {
    long startDays = start->year * 365 + start->month * 30 + start->day;
    long endDays = end->year * 365 + end->month * 30 + end->day;
    return endDays - startDays;
}

// Initialize library
void initLibrary(Library *lib) {
    lib->bookCount = 0;
    lib->memberCount = 0;
    lib->loanCount = 0;
    lib->reservationCount = 0;
}

// Save library data to files
void saveLibrary(Library *lib) {
    FILE *file;
    
    file = fopen("books.dat", "w");
    if (file) {
        for (int i = 0; i < lib->bookCount; i++) {
            Book *b = &lib->books[i];
            fprintf(file, "%s|%s|%s|%s|%d|%s|%d|%d\n",
                    b->bookId, b->title, b->author, b->isbn,
                    b->publicationYear, b->category, b->totalCopies, b->availableCopies);
        }
        fclose(file);
    }

    file = fopen("members.dat", "w");
    if (file) {
        for (int i = 0; i < lib->memberCount; i++) {
            Member *m = &lib->members[i];
            char joinDateStr[11];
            formatDate(&m->joinDate, joinDateStr);
            fprintf(file, "%s|%s|%s|%s|%s|%s|%s|%s\n",
                    m->memberId, m->firstName, m->lastName, m->email,
                    m->phone, m->address, joinDateStr, m->status);
        }
        fclose(file);
    }

    file = fopen("loans.dat", "w");
    if (file) {
        for (int i = 0; i < lib->loanCount; i++) {
            Loan *l = &lib->loans[i];
            char loanDateStr[11], dueDateStr[11], returnDateStr[11] = "NULL";
            formatDate(&l->loanDate, loanDateStr);
            formatDate(&l->dueDate, dueDateStr);
            if (l->isReturned) {
                formatDate(&l->returnDate, returnDateStr);
            }
            fprintf(file, "%s|%s|%s|%s|%s|%s\n",
                    l->loanId, l->bookId, l->memberId,
                    loanDateStr, dueDateStr, returnDateStr);
        }
        fclose(file);
    }

    file = fopen("reservations.dat", "w");
    if (file) {
        for (int i = 0; i < lib->reservationCount; i++) {
            Reservation *r = &lib->reservations[i];
            char resDateStr[11], expDateStr[11];
            formatDate(&r->reservationDate, resDateStr);
            formatDate(&r->expiryDate, expDateStr);
            fprintf(file, "%s|%s|%s|%s|%s|%s\n",
                    r->reservationId, r->bookId, r->memberId,
                    resDateStr, expDateStr, r->status);
        }
        fclose(file);
    }
}

// Load library data from files
void loadLibrary(Library *lib) {
    FILE *file;
    char line[512];

    file = fopen("books.dat", "r");
    if (file) {
        while (fgets(line, sizeof(line), file) && lib->bookCount < MAX_BOOKS) {
            Book *b = &lib->books[lib->bookCount];
            sscanf(line, "%[^|]|%[^|]|%[^|]|%[^|]|%d|%[^|]|%d|%d\n",
                   b->bookId, b->title, b->author, b->isbn,
                   &b->publicationYear, b->category, &b->totalCopies, &b->availableCopies);
            lib->bookCount++;
        }
        fclose(file);
    }

    file = fopen("members.dat", "r");
    if (file) {
        while (fgets(line, sizeof(line), file) && lib->memberCount < MAX_MEMBERS) {
            Member *m = &lib->members[lib->memberCount];
            char joinDateStr[11];
            sscanf(line, "%[^|]|%[^|]|%[^|]|%[^|]|%[^|]|%[^|]|%[^|]|%s\n",
                   m->memberId, m->firstName, m->lastName, m->email,
                   m->phone, m->address, joinDateStr, m->status);
            parseDate(joinDateStr, &m->joinDate);
            lib->memberCount++;
        }
        fclose(file);
    }

    file = fopen("loans.dat", "r");
    if (file) {
        while (fgets(line, sizeof(line), file) && lib->loanCount < MAX_LOANS) {
            Loan *l = &lib->loans[lib->loanCount];
            char loanDateStr[11], dueDateStr[11], returnDateStr[11];
            sscanf(line, "%[^|]|%[^|]|%[^|]|%[^|]|%[^|]|%s\n",
                   l->loanId, l->bookId, l->memberId,
                   loanDateStr, dueDateStr, returnDateStr);
            parseDate(loanDateStr, &l->loanDate);
            parseDate(dueDateStr, &l->dueDate);
            l->isReturned = strcmp(returnDateStr, "NULL") != 0;
            if (l->isReturned) {
                parseDate(returnDateStr, &l->returnDate);
            }
            lib->loanCount++;
        }
        fclose(file);
    }

    file = fopen("reservations.dat", "r");
    if (file) {
        while (fgets(line, sizeof(line), file) && lib->reservationCount < MAX_RESERVATIONS) {
            Reservation *r = &lib->reservations[lib->reservationCount];
            char resDateStr[11], expDateStr[11];
            sscanf(line, "%[^|]|%[^|]|%[^|]|%[^|]|%[^|]|%s\n",
                   r->reservationId, r->bookId, r->memberId,
                   resDateStr, expDateStr, r->status);
            parseDate(resDateStr, &r->reservationDate);
            parseDate(expDateStr, &r->expiryDate);
            lib->reservationCount++;
        }
        fclose(file);
    }
}

// Add book
int addBook(Library *lib, const char *title, const char *author, const char *isbn, int year, const char *category, int copies) {
    if (lib->bookCount >= MAX_BOOKS) {
        printf("Book limit reached.\n");
        return 0;
    }
    Book *b = &lib->books[lib->bookCount];
    generateUUID(b->bookId);
    strncpy(b->title, title, MAX_STR - 1);
    strncpy(b->author, author, MAX_STR - 1);
    strncpy(b->isbn, isbn, 13);
    b->publicationYear = year;
    strncpy(b->category, category, MAX_STR - 1);
    b->totalCopies = copies;
    b->availableCopies = copies;
    lib->bookCount++;
    saveLibrary(lib);
    printf("Book added: %s\n", title);
    return 1;
}

// Add member
int addMember(Library *lib, const char *firstName, const char *lastName, const char *email, const char *phone, const char *address) {
    if (lib->memberCount >= MAX_MEMBERS) {
        printf("Member limit reached.\n");
        return 0;
    }
    Member *m = &lib->members[lib->memberCount];
    generateUUID(m->memberId);
    strncpy(m->firstName, firstName, MAX_STR - 1);
    strncpy(m->lastName, lastName, MAX_STR - 1);
    strncpy(m->email, email, MAX_STR - 1);
    strncpy(m->phone, phone, 19);
    strncpy(m->address, address, MAX_STR - 1);
    getCurrentDate(&m->joinDate);
    strcpy(m->status, "Active");
    lib->memberCount++;
    saveLibrary(lib);
    printf("Member added: %s %s\n", firstName, lastName);
    return 1;
}

// Borrow book
int borrowBook(Library *lib, const char *bookId, const char *memberId) {
    Book *book = NULL;
    Member *member = NULL;
    
    for (int i = 0; i < lib->bookCount; i++) {
        if (strcmp(lib->books[i].bookId, bookId) == 0) {
            book = &lib->books[i];
            break;
        }
    }
    for (int i = 0; i < lib->memberCount; i++) {
        if (strcmp(lib->members[i].memberId, memberId) == 0) {
            member = &lib->members[i];
            break;
        }
    }

    if (!book) {
        printf("Book not found.\n");
        return 0;
    }
    if (!member) {
        printf("Member not found.\n");
        return 0;
    }
    if (strcmp(member->status, "Active") != 0) {
        printf("Member is not active.\n");
        return 0;
    }
    if (book->availableCopies <= 0) {
        printf("No copies available.\n");
        return 0;
    }
    if (lib->loanCount >= MAX_LOANS) {
        printf("Loan limit reached.\n");
        return 0;
    }

    Loan *loan = &lib->loans[lib->loanCount];
    generateUUID(loan->loanId);
    strcpy(loan->bookId, bookId);
    strcpy(loan->memberId, memberId);
    getCurrentDate(&loan->loanDate);
    addDaysToDate(&loan->loanDate, LOAN_PERIOD_DAYS, &loan->dueDate);
    loan->isReturned = 0;
    book->availableCopies--;
    lib->loanCount++;
    saveLibrary(lib);
    printf("Book borrowed: %s by %s %s\n", book->title, member->firstName, member->lastName);
    return 1;
}

// Return book
int returnBook(Library *lib, const char *loanId, const char *returnDateStr) {
    Loan *loan = NULL;
    Book *book = NULL;
    
    for (int i = 0; i < lib->loanCount; i++) {
        if (strcmp(lib->loans[i].loanId, loanId) == 0) {
            loan = &lib->loans[i];
            break;
        }
    }
    if (!loan || loan->isReturned) {
        printf("Loan not found or already returned.\n");
        return 0;
    }

    for (int i = 0; i < lib->bookCount; i++) {
        if (strcmp(lib->books[i].bookId, loan->bookId) == 0) {
            book = &lib->books[i];
            break;
        }
    }
    if (!book) {
        printf("Book not found.\n");
        return 0;
    }

    Date returnDate;
    if (!parseDate(returnDateStr, &returnDate)) {
        printf("Invalid date format.\n");
        return 0;
    }

    loan->returnDate = returnDate;
    loan->isReturned = 1;
    book->availableCopies++;
    long daysOverdue = daysBetweenDates(&loan->dueDate, &returnDate);
    if (daysOverdue > 0) {
        double fine = daysOverdue * FINE_PER_DAY;
        printf("Fine incurred: $%.2f\n", fine);
    }
    saveLibrary(lib);
    printf("Book returned: %s\n", book->title);
    return 1;
}

// Reserve book
int reserveBook(Library *lib, const char *bookId, const char *memberId) {
    Book *book = NULL;
    Member *member = NULL;
    
    for (int i = 0; i < lib->bookCount; i++) {
        if (strcmp(lib->books[i].bookId, bookId) == 0) {
            book = &lib->books[i];
            break;
        }
    }
    for (int i = 0; i < lib->memberCount; i++) {
        if (strcmp(lib->members[i].memberId, memberId) == 0) {
            member = &lib->members[i];
            break;
        }
    }

    if (!book) {
        printf("Book not found.\n");
        return 0;
    }
    if (!member) {
        printf("Member not found.\n");
        return 0;
    }
    if (strcmp(member->status, "Active") != 0) {
        printf("Member is not active.\n");
        return 0;
    }
    int activeLoans = 0;
    for (int i = 0; i < lib->loanCount; i++) {
        if (strcmp(lib->loans[i].memberId, memberId) == 0 && !lib->loans[i].isReturned) {
            activeLoans++;
        }
    }
    if (activeLoans >= 3) {
        printf("Too many active loans.\n");
        return 0;
    }
    if (lib->reservationCount >= MAX_RESERVATIONS) {
        printf("Reservation limit reached.\n");
        return 0;
    }

    Reservation *res = &lib->reservations[lib->reservationCount];
    generateUUID(res->reservationId);
    strcpy(res->bookId, bookId);
    strcpy(res->memberId, memberId);
    getCurrentDate(&res->reservationDate);
    addDaysToDate(&res->reservationDate, 7, &res->expiryDate);
    strcpy(res->status, "Active");
    lib->reservationCount++;
    saveLibrary(lib);
    printf("Book reserved: %s for %s %s\n", book->title, member->firstName, member->lastName);
    return 1;
}

// List all books
void listBooks(Library *lib) {
    if (lib->bookCount == 0) {
        printf("No books available.\n");
        return;
    }
    printf("\nBooks:\n");
    for (int i = 0; i < lib->bookCount; i++) {
        Book *b = &lib->books[i];
        printf("ID: %s, Title: %s, Author: %s, ISBN: %s, Year: %d, Category: %s, Copies: %d/%d\n",
               b->bookId, b->title, b->author, b->isbn,
               b->publicationYear, b->category, b->availableCopies, b->totalCopies);
    }
}

// List all members
void listMembers(Library *lib) {
    if (lib->memberCount == 0) {
        printf("No members registered.\n");
        return;
    }
    printf("\nMembers:\n");
    for (int i = 0; i < lib->memberCount; i++) {
        Member *m = &lib->members[i];
        char joinDateStr[11];
        formatDate(&m->joinDate, joinDateStr);
        printf("ID: %s, Name: %s %s, Email: %s, Phone: %s, Address: %s, Join Date: %s, Status: %s\n",
               m->memberId, m->firstName, m->lastName, m->email,
               m->phone, m->address, joinDateStr, m->status);
    }
}

// List active loans
void listActiveLoans(Library *lib) {
    int found = 0;
    printf("\nActive Loans:\n");
    for (int i = 0; i < lib->loanCount; i++) {
        if (!lib->loans[i].isReturned) {
            Loan *l = &lib->loans[i];
            Book *b = NULL;
            Member *m = NULL;
            for (int j = 0; j < lib->bookCount; j++) {
                if (strcmp(lib->books[j].bookId, l->bookId) == 0) {
                    b = &lib->books[j];
                    break;
                }
            }
            for (int j = 0; j < lib->memberCount; j++) {
                if (strcmp(lib->members[j].memberId, l->memberId) == 0) {
                    m = &lib->members[j];
                    break;
                }
            }
            char loanDateStr[11], dueDateStr[11];
            formatDate(&l->loanDate, loanDateStr);
            formatDate(&l->dueDate, dueDateStr);
            printf("Loan ID: %s, Book: %s, Member: %s %s, Loan Date: %s, Due Date: %s\n",
                   l->loanId, b ? b->title : "Unknown",
                   m ? m->firstName : "Unknown", m ? m->lastName : "",
                   loanDateStr, dueDateStr);
            found = 1;
        }
    }
    if (!found) {
        printf("No active loans.\n");
    }
}

// List overdue loans
void listOverdueLoans(Library *lib) {
    Date today;
    getCurrentDate(&today);
    int found = 0;
    printf("\nOverdue Loans:\n");
    for (int i = 0; i < lib->loanCount; i++) {
        if (!lib->loans[i].isReturned && daysBetweenDates(&lib->loans[i].dueDate, &today) > 0) {
            Loan *l = &lib->loans[i];
            Book *b = NULL;
            Member *m = NULL;
            for (int j = 0; j < lib->bookCount; j++) {
                if (strcmp(lib->books[j].bookId, l->bookId) == 0) {
                    b = &lib->books[j];
                    break;
                }
            }
            for (int j = 0; j < lib->memberCount; j++) {
                if (strcmp(lib->members[j].memberId, l->memberId) == 0) {
                    m = &lib->members[j];
                    break;
                }
            }
            char dueDateStr[11];
            formatDate(&l->dueDate, dueDateStr);
            long daysOverdue = daysBetweenDates(&l->dueDate, &today);
            printf("Loan ID: %s, Book: %s, Member: %s %s, Due Date: %s, Days Overdue: %ld\n",
                   l->loanId, b ? b->title : "Unknown",
                   m ? m->firstName : "Unknown", m ? m->lastName : "",
                   dueDateStr, daysOverdue);
            found = 1;
        }
    }
    if (!found) {
        printf("No overdue loans.\n");
    }
}

// Main menu
void menu(Library *lib) {
    char input[256], bookId[37], memberId[37], loanId[37], dateStr[11];
    int choice;

    while (1) {
        printf("\n=== Library Management System ===\n");
        printf("1. Add Book\n2. Add Member\n3. Borrow Book\n4. Return Book\n5. Reserve Book\n");
        printf("6. List Books\n7. List Members\n8. List Active Loans\n9. List Overdue Loans\n10. Exit\n");
        printf("Choice: ");
        if (!fgets(input, sizeof(input), stdin)) continue;
        if (sscanf(input, "%d", &choice) != 1) {
            printf("Invalid input.\n");
            continue;
        }

        switch (choice) {
            case 1: {
                char title[MAX_STR], author[MAX_STR], isbn[14], category[MAX_STR];
                int year, copies;
                printf("Title: ");
                fgets(title, MAX_STR, stdin);
                title[strcspn(title, "\n")] = 0;
                printf("Author: ");
                fgets(author, MAX_STR, stdin);
                author[strcspn(author, "\n")] = 0;
                printf("ISBN: ");
                fgets(isbn, 14, stdin);
                isbn[strcspn(isbn, "\n")] = 0;
                printf("Publication Year: ");
                fgets(input, sizeof(input), stdin);
                sscanf(input, "%d", &year);
                printf("Category: ");
                fgets(category, MAX_STR, stdin);
                category[strcspn(category, "\n")] = 0;
                printf("Total Copies: ");
                fgets(input, sizeof(input), stdin);
                sscanf(input, "%d", &copies);
                addBook(lib, title, author, isbn, year, category, copies);
                break;
            }
            case 2: {
                char firstName[MAX_STR], lastName[MAX_STR], email[MAX_STR], phone[20], address[MAX_STR];
                printf("First Name: ");
                fgets(firstName, MAX_STR, stdin);
                firstName[strcspn(firstName, "\n")] = 0;
                printf("Last Name: ");
                fgets(lastName, MAX_STR, stdin);
                lastName[strcspn(lastName, "\n")] = 0;
                printf("Email: ");
                fgets(email, MAX_STR, stdin);
                email[strcspn(email, "\n")] = 0;
                printf("Phone: ");
                fgets(phone, 20, stdin);
                phone[strcspn(phone, "\n")] = 0;
                printf("Address: ");
                fgets(address, MAX_STR, stdin);
                address[strcspn(address, "\n")] = 0;
                addMember(lib, firstName, lastName, email, phone, address);
                break;
            }
            case 3:
                printf("Book ID: ");
                fgets(bookId, 37, stdin);
                bookId[strcspn(bookId, "\n")] = 0;
                printf("Member ID: ");
                fgets(memberId, 37, stdin);
                memberId[strcspn(memberId, "\n")] = 0;
                borrowBook(lib, bookId, memberId);
                break;
            case 4:
                printf("Loan ID: ");
                fgets(loanId, 37, stdin);
                loanId[strcspn(loanId, "\n")] = 0;
                printf("Return Date (YYYY-MM-DD): ");
                fgets(dateStr, 11, stdin);
                dateStr[strcspn(dateStr, "\n")] = 0;
                returnBook(lib, loanId, dateStr);
                break;
            case 5:
                printf("Book ID: ");
                fgets(bookId, 37, stdin);
                bookId[strcspn(bookId, "\n")] = 0;
                printf("Member ID: ");
                fgets(memberId, 37, stdin);
                memberId[strcspn(memberId, "\n")] = 0;
                reserveBook(lib, bookId, memberId);
                break;
            case 6:
                listBooks(lib);
                break;
            case 7:
                listMembers(lib);
                break;
            case 8:
                listActiveLoans(lib);
                break;
            case 9:
                listOverdueLoans(lib);
                break;
            case 10:
                printf("Exiting...\n");
                saveLibrary(lib);
                return;
            default:
                printf("Invalid choice.\n");
        }
    }
}

// Main function with sample data
int main() {
    srand(time(NULL));
    Library lib;
    initLibrary(&lib);
    loadLibrary(&lib);

    // Add sample books
    addBook(&lib, "The Great Adventure", "John Smith", "9781234567890", 2010, "Fiction", 5);
    addBook(&lib, "Science Unveiled", "Emma Johnson", "9781234567891", 2015, "Science", 3);
    addBook(&lib, "History of Time", "Michael Brown", "9781234567892", 2008, "History", 4);
    addBook(&lib, "Mystic Realms", "Sarah Davis", "9781234567893", 2018, "Fantasy", 6);
    addBook(&lib, "Murder Mystery", "David Wilson", "9781234567894", 2020, "Mystery", 5);
    addBook(&lib, "Life Lessons", "Jane Taylor", "9781234567895", 2019, "Self-Help", 3);
    addBook(&lib, "Tech Revolution", "Robert Anderson", "9781234567896", 2021, "Technology", 4);
    addBook(&lib, "Kids Tales", "Emily White", "9781234567897", 2017, "Children", 7);
    addBook(&lib, "Biography of a Hero", "Thomas Harris", "9781234567898", 2016, "Biography", 3);
    addBook(&lib, "Future Visions", "Laura Martin", "9781234567899", 2022, "Science", 5);
    addBook(&lib, "The Lost Kingdom", "John Smith", "9781234567900", 2011, "Fiction", 4);
    addBook(&lib, "Quantum Physics", "Emma Johnson", "9781234567901", 2014, "Science", 3);
    addBook(&lib, "Ancient Civilizations", "Michael Brown", "9781234567902", 2009, "History", 5);
    addBook(&lib, "Dragon Tales", "Sarah Davis", "9781234567903", 2019, "Fantasy", 6);
    addBook(&lib, "The Hidden Clue", "David Wilson", "9781234567904", 2021, "Mystery", 4);
    addBook(&lib, "Grow Yourself", "Jane Taylor", "9781234567905", 2020, "Self-Help", 3);
    addBook(&lib, "AI Revolution", "Robert Anderson", "9781234567906", 2022, "Technology", 5);
    addBook(&lib, "Magic Adventures", "Emily White", "9781234567907", 2018, "Children", 6);
    addBook(&lib, "A Life Story", "Thomas Harris", "9781234567908", 2017, "Biography", 4);
    addBook(&lib, "Space Exploration", "Laura Martin", "9781234567909", 2023, "Science", 5);
    addBook(&lib, "The Silent Forest", "John Smith", "9781234567910", 2012, "Fiction", 4);
    addBook(&lib, "Physics of Tomorrow", "Emma Johnson", "9781234567911", 2016, "Science", 3);
    addBook(&lib, "War and Peace", "Michael Brown", "9781234567912", 2010, "History", 5);
    addBook(&lib, "Enchanted Lands", "Sarah Davis", "9781234567913", 2020, "Fantasy", 6);
    addBook(&lib, "The Secret Code", "David Wilson", "9781234567914", 2022, "Mystery", 4);
    addBook(&lib, "Mindful Living", "Jane Taylor", "9781234567915", 2021, "Self-Help", 3);
    addBook(&lib, "Digital Future", "Robert Anderson", "9781234567916", 2023, "Technology", 5);
    addBook(&lib, "Fairy Tales", "Emily White", "9781234567917", 2019, "Children", 6);
    addBook(&lib, "Legendary Lives", "Thomas Harris", "9781234567918", 2018, "Biography", 4);
    addBook(&lib, "Cosmic Journey", "Laura Martin", "9781234567919", 2024, "Science", 5);

    // Add sample members
    addMember(&lib, "Alice", "Smith", "alice.smith@email.com", "555-1001", "123 Main St, NY");
    addMember(&lib, "Bob", "Johnson", "bob.johnson@email.com", "555-1002", "456 Oak Ave, CA");
    addMember(&lib, "Carol", "Williams", "carol.williams@email.com", "555-1003", "789 Pine Rd, TX");
    addMember(&lib, "David", "Brown", "david.brown@email.com", "555-1004", "101 Elm St, FL");
    addMember(&lib, "Eve", "Davis", "eve.davis@email.com", "555-1005", "202 Cedar Ln, NY");
    addMember(&lib, "Frank", "Wilson", "frank.wilson@email.com", "555-1006", "303 Maple Dr, CA");
    addMember(&lib, "Grace", "Taylor", "grace.taylor@email.com", "555-1007", "404 Birch Ave, TX");
    addMember(&lib, "Henry", "Anderson", "henry.anderson@email.com", "555-1008", "505 Spruce St, FL");
    addMember(&lib, "Isabel", "Thomas", "isabel.thomas@email.com", "555-1009", "606 Willow Rd, NY");
    addMember(&lib, "Jack", "Martin", "jack.martin@email.com", "555-1010", "707 Oak St, CA");
    addMember(&lib, "Kelly", "Green", "kelly.green@email.com", "555-1011", "808 Pine St, TX");
    addMember(&lib, "Liam", "Walker", "liam.walker@email.com", "555-1012", "909 Cedar Ave, CA");
    addMember(&lib, "Mia", "Hall", "mia.hall@email.com", "555-1013", "1010 Oak Rd, NY");
    addMember(&lib, "Noah", "Allen", "noah.allen@email.com", "555-1014", "1111 Elm St, FL");
    addMember(&lib, "Olivia", "Young", "olivia.young@email.com", "555-1015", "1212 Maple Dr, TX");
    addMember(&lib, "Peter", "King", "peter.king@email.com", "555-1016", "1313 Birch Ave, CA");
    addMember(&lib, "Quinn", "Scott", "quinn.scott@email.com", "555-1017", "1414 Spruce St, NY");
    addMember(&lib, "Rachel", "Adams", "rachel.adams@email.com", "555-1018", "1515 Willow Rd, FL");
    addMember(&lib, "Sam", "Baker", "sam.baker@email.com", "555-1019", "1616 Oak St, TX");
    addMember(&lib, "Tina", "Clark", "tina.clark@email.com", "555-1020", "1717 Pine Ave, CA");

    // Start menu
    menu(&lib);
    return 0;
}
