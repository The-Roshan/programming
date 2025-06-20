#include <iostream>
using namespace std;
class Calculator {
private:
double num1;
double num2;
public:
// Constructor
Calculator(double n1, double n2) : num1(n1), num2(n2) {}
// Destructor
~Calculator() {}
// Member functions to perform calculations
double add() {
return num1 + num2;
}
double subtract() {
return num1 - num2;
}
double multiply() {
return num1 * num2;
}
double divide() {
if (num2 == 0) {
throw invalid_argument("Division by zero is not allowed.");
}
return num1 / num2;
}
};
int main() {
double num1, num2;
cout << "Enter first number: ";
cin >> num1;
cout << "Enter second number: ";
cin >> num2;
Calculator calc(num1, num2);
cout << "Addition: " << calc.add() << endl;
cout << "Subtraction: " << calc.subtract() << endl;
cout << "Multiplication: " << calc.multiply() << endl;
try {
cout << "Division: " << calc.divide() << endl;
} catch (const invalid_argument& e) {
cerr << "Error: " << e.what() << endl;
}
return 0;
}
