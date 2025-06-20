#include <iostream>
#include <cmath>
using namespace std;
int main() {
double a, b, c;
cout << "Enter coefficients a, b, and c: ";
cin >> a >> b >> c;
double discriminant = b * b - 4 * a * c;
if (discriminant > 0) {
double root1 = (-b + sqrt(discriminant)) / (2 * a);
double root2 = (-b - sqrt(discriminant)) / (2 * a);
cout << "Two distinct real roots:\n";
cout << "Root 1: " << root1 << "\n";
cout << "Root 2: " << root2 << "\n";
} else if (discriminant == 0) {
double root = -b / (2 * a);
cout << "Two equal roots:\n";
cout << "Root 1: " << root << "\n";
cout << "Root 2: " << root << "\n";
} else {
double realPart = -b / (2 * a);
double imaginaryPart = sqrt(abs(discriminant)) / (2 * a);
cout << "Two distinct complex roots:\n";
cout << "Root 1: " << realPart << " + " << imaginaryPart << "i\n";
cout << "Root 2: " << realPart << " - " << imaginaryPart << "i\n";
}
return 0;
}
