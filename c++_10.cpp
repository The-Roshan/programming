#include <iostream>
using namespace std;
class Number {
private:
int num;
public:
// Constructors
Number() : num(0) {} // Default constructor
Number(int n) : num(n) {} // Parameterized constructor
// Function to input data
void input() {
cin >> num;
}
// Function to display data
void display() const {
cout << num << endl;
}
// Friend function to find the sum of two Number objects
friend Number operator+(const Number& num1, const Number& num2);
};
// Overloading the + operator
Number operator+(const Number& num1, const Number& num2) {
Number result;
result.num = num1.num + num2.num;
return result;
}
int main() {
Number num1, num2;
cout << "Enter the first number: ";
num1.input();
cout << "Enter the second number: ";
num2.input();
Number sum = num1 + num2;
cout << "The sum of the two numbers is: ";
sum.display();
return 0;
}
