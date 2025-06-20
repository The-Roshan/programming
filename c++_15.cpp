#include <iostream>
using namespace std;
// Class representing a point in 2D space
class Point {
private:
int x, y;
public:
// Constructor
Point(int x = 0, int y = 0) : x(x), y(y) {}
// Getter methods
int getX() const { return x; }
int getY() const { return y; }
// Setter methods
void setX(int newX) { x = newX; }
void setY(int newY) { y = newY; }
};
// Conversion function from int to Point
Point intToPoint(int value) {
return Point(value, value); // Convert int value to Point
}
int main() {
int intValue;
cout << "Enter an integer value: ";
cin >> intValue;
Point point = intToPoint(intValue); // Conversion from int to Point
cout << "Point coordinates: (" << point.getX() << ", " << point.getY() << ")" << endl;
return 0;
}
