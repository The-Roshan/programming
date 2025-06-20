#include <iostream>
#include <cmath>

using namespace std;

class Shape {
public:
    virtual double area() const = 0;
};

class Square : public Shape {
private:
    double side;
public:
    Square(double s) : side(s) {}

    double area() const override {
        return side * side;
    }
};

class Rectangle : public Shape {
private:
    double length;
    double width;
public:
    Rectangle(double l, double w) : length(l), width(w) {}

    double area() const override {
        return length * width;
    }
};

class Triangle : public Shape {
private:
    double base;
    double height;
public:
    Triangle(double b, double h) : base(b), height(h) {}

    double area() const override {
        return 0.5 * base * height;
    }
};

int main() {
    int choice;
    double s, l, w, b, h;

    do {
        cout << "Choose the shape to calculate area:\n";
        cout << "1. Square\n";
        cout << "2. Rectangle\n";
        cout << "3. Triangle\n";
        cout << "4. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter the side length of the square: ";
                cin >> s;
                cout << "Area of the square: " << Square(s).area() << endl;
                break;
            case 2:
                cout << "Enter the length and width of the rectangle: ";
                cin >> l >> w;
                cout << "Area of the rectangle: " << Rectangle(l, w).area() << endl;
                break;
            case 3:
                cout << "Enter the base and height of the triangle: ";
                cin >> b >> h;
                cout << "Area of the triangle: " << Triangle(b, h).area() << endl;
                break;
            case 4:
                cout << "Exiting the program..." << endl;
                break;
            default:
                cout << "Invalid choice! Please choose a valid option." << endl;
                break;
        }

    } while (choice != 4);

    return 0;
}
