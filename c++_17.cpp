#include <iostream>
#include <fstream>
#include <cstring>
using namespace std;
// Employee structure
struct Employee {
int id;
char name[50];
float salary;
};
// Function prototypes
void insertRecord(const char* fileName);
void displayRecords(const char* fileName);
void searchRecord(const char* fileName, int searchId);
void deleteRecord(const char* fileName, int deleteId);
int main() {
const char* fileName = "employees.bin";
int choice;
do {
cout << "\nEmployee Management System\n";
cout << "1. Insert Record\n";
cout << "2. Display Records\n";
cout << "3. Search Record\n";
cout << "4. Delete Record\n";
cout << "5. Exit\n";
cout << "Enter your choice: ";
cin >> choice;
switch(choice) {
case 1:
insertRecord(fileName);
break;
case 2:
displayRecords(fileName);
break;
case 3: {
int searchId;
cout << "Enter Employee ID to search: ";
cin >> searchId;
searchRecord(fileName, searchId);
break;
}
case 4: {
int deleteId;
cout << "Enter Employee ID to delete: ";
cin >> deleteId;
deleteRecord(fileName, deleteId);
break;
}
case 5:
cout << "Exiting...";
break;
default:
cout << "Invalid choice!";
}
} while(choice != 5);
return 0;
}
// Function to insert record into binary file
void insertRecord(const char* fileName) {
Employee emp;
ofstream outFile(fileName, ios::binary | ios::app);
if (!outFile) {
cerr << "Failed to open file!" << endl;
return;
}
cout << "\nEnter Employee ID: ";
cin >> emp.id;
cout << "Enter Employee Name: ";
cin.ignore();
cin.getline(emp.name, 50);
cout << "Enter Employee Salary: ";
cin >> emp.salary;
outFile.write(reinterpret_cast<char*>(&emp), sizeof(Employee));
cout << "Record inserted successfully!" << endl;
outFile.close();
}
// Function to display all records from binary file
void displayRecords(const char* fileName) {
ifstream inFile(fileName, ios::binary);
if (!inFile) {
cerr << "Failed to open file!" << endl;
return;
}
Employee emp;
while (inFile.read(reinterpret_cast<char*>(&emp), sizeof(Employee))) {
cout << "ID: " << emp.id << ", Name: " << emp.name << ", Salary: " << emp.salary
<< endl;
}
inFile.close();
}
// Function to search record by ID from binary file
void searchRecord(const char* fileName, int searchId) {
ifstream inFile(fileName, ios::binary);
if (!inFile) {
cerr << "Failed to open file!" << endl;
return;
}
Employee emp;
bool found = false;
while (inFile.read(reinterpret_cast<char*>(&emp), sizeof(Employee))) {
if (emp.id == searchId) {
cout << "Record found: " << endl;
cout << "ID: " << emp.id << ", Name: " << emp.name << ", Salary: " <<
emp.salary << endl;
found = true;
break;
}
}
if (!found) {
cout << "Record with ID " << searchId << " not found!" << endl;
}
inFile.close();
}
// Function to delete record by ID from binary file
void deleteRecord(const char* fileName, int deleteId) {
ifstream inFile(fileName, ios::binary);
if (!inFile) {
cerr << "Failed to open file!" << endl;
return;
}
ofstream tempFile("temp.bin", ios::binary);
if (!tempFile) {
cerr << "Failed to create temporary file!" << endl;
inFile.close();
return;
}
Employee emp;
bool found = false;
while (inFile.read(reinterpret_cast<char*>(&emp), sizeof(Employee))) {
if (emp.id != deleteId) {
tempFile.write(reinterpret_cast<char*>(&emp), sizeof(Employee));
} else {
found = true;
}
}
inFile.close();
tempFile.close();
if (!found) {
cout << "Record with ID " << deleteId << " not found!" << endl;
remove("temp.bin");
} else {
remove(fileName);
rename("temp.bin", fileName);
cout << "Record deleted successfully!" << endl;
}
}