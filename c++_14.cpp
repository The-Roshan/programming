#include <iostream>
#include <cstring>
using namespace std;
class MyString {
private:
char* str;
public:
// Constructor
MyString(const char* s = "") {
str = new char[strlen(s) + 1];
strcpy(str, s);
}
// Destructor
~MyString() {
delete[] str;
}
// Overloading == operator
bool operator==(const MyString& other) const {
return strcmp(str, other.str) == 0;
}
};
int main() {
char input1[100], input2[100];
// Input for first string
cout << "Enter the first string: ";
cin.getline(input1, 100);
// Input for second string
cout << "Enter the second string: ";
cin.getline(input2, 100);
// Create MyString objects
MyString str1(input1);
MyString str2(input2);
// Compare strings
if (str1 == str2) {
cout << "The two strings are equal." << endl;
} else {
cout << "The two strings are not equal." << endl;
}
return 0;
}
