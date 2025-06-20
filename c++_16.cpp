#include <iostream>
using namespace std;
// Base class
class Shape {
protected:
double dimension1;
double dimension2;
public:
// Member function to initialize data members
void get_data() {
cout << "Enter dimension 1: ";
cin >> dimension1;
cout << "Enter dimension 2: ";
cin >> dimension2;
}
// Virtual function to compute and display area
virtual void display_area() {
cout << "Area: " << endl;
}
};
// Derived class for Triangle
class Triangle : public Shape {
public:
// Redefining display_area() for triangles
void display_area() override {
cout << "Area of Triangle: " << 0.5 * dimension1 * dimension2 << endl;
}
};
// Derived class for Rectangle
class Rectangle : public Shape {
public:
// Redefining display_area() for rectangles
void display_area() override {
cout << "Area of Rectangle: " << dimension1 * dimension2 << endl;
}
};
int main() {
Shape *shapePtr;
char choice;
cout << "Enter 't' for Triangle or 'r' for Rectangle: ";
cin >> choice;
if (choice == 't') {
shapePtr = new Triangle();
} else if (choice == 'r') {
shapePtr = new Rectangle();
} else {
cout << "Invalid choice!" << endl;
return 1;
}
shapePtr->get_data(); // Get dimensions from user
shapePtr->display_area(); // Display area using polymorphism
delete shapePtr; // Free allocated memory
return 0;
}
