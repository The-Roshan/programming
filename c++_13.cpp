#include <iostream>
using namespace std;
class Complex {
private:
double real;
double imag;
public:
// Constructor
Complex(double r = 0.0, double i = 0.0) : real(r), imag(i) {}
// Overloading + operator
Complex operator+(const Complex& obj) {
Complex temp;
temp.real = real + obj.real;
temp.imag = imag + obj.imag;
return temp;
}
// Function to display complex number
void display() {
cout << "Real part: " << real << ", Imaginary part: " << imag << "i" << endl;
}
};
int main() {
double real1, imag1, real2, imag2;
// Input for first complex number
cout << "Enter real part of first complex number: ";
cin >> real1;
cout << "Enter imaginary part of first complex number: ";
cin >> imag1;
// Input for second complex number
cout << "Enter real part of second complex number: ";
cin >> real2;
cout << "Enter imaginary part of second complex number: ";
cin >> imag2;
// Define complex numbers
Complex c1(real1, imag1);
Complex c2(real2, imag2);
Complex sum;
// Sum of complex numbers using overloaded + operator
sum = c1 + c2;
// Display the result
cout << "Sum of two complex numbers:" << endl;
sum.display();
return 0;
}
