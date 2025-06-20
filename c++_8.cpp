#include <iostream>
using namespace std;
// Function to swap values using call by value
void swapByValue(int a, int b) {
int temp = a;
a = b;
b = temp;
cout << "\nInside swapByValue function: a = " << a << ", b = " << b << endl;
}
// Function to swap values using call by reference
void swapByReference(int* a, int* b) {
int temp = *a;
*a = *b;
*b = temp;
cout << "\nInside swapByReference function: a = " << *a << ", b = " << *b << endl;
}
int main() {
int num1, num2;
cout << "Enter two integers: ";
cin >> num1 >> num2;
cout << "\nBefore swapping: " << endl;
cout << "num1 = " << num1 << ", num2 = " << num2 << endl;
// Call swapByValue function
swapByValue(num1, num2);
cout << "\nAfter calling swapByValue function: " << endl;
cout << "num1 = " << num1 << ", num2 = " << num2 << endl;
// Call swapByReference function
swapByReference(&num1, &num2);
cout << "\nAfter calling swapByReference function: " << endl;
cout << "num1 = " << num1 << ", num2 = " << num2 << endl;
return 0;
}
