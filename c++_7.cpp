#include <iostream>
#include <cmath>
using namespace std;
int calculate(int x, int y = 0, int z = 0) {
if (y == 0 || z == 0) {
return x * x; // Only x is passed
} else if (z == 0) {
return pow(x, y); // x raised to the power of y
} else {
return pow(x, y) + pow(x, z); // x raised to the power of y plus x raised to the power of z
}
}
int main() {
int x, y, z;
cout << "Enter value for x: ";
cin >> x;
// Prompt for y if needed
if (x != 0) {
cout << "Enter value for y: ";
cin >> y;
}
// Prompt for z if needed
if (y != 0) {
cout << "Enter value for z: ";
cin >> z;
}
// Calculate and display the result
int result = calculate(x, y, z);
cout << "Result: " << result << endl;
return 0;
}
