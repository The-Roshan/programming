//Write a Java program to create a shape class and derive, square and circle classes from shape
//class. Define appropriate constructor for all the three classes. Define a method Area( ) to calculate
//area of circle and square in respective class. Assume PI = 3.14 and
//declare it as a final variable in circle class.

import java.util.Scanner;

// Base Shape class
class Shape {
    public Shape() {
        // Constructor for Shape
    }
}

// Derived Square class
class Square extends Shape {
    private double side;

    public Square(double side) {
        this.side = side;
    }

    public double Area() {
        return side * side;
    }
}

// Derived Circle class
class Circle extends Shape {
    private double radius;
    private final double PI = 3.14;

    public Circle(double radius) {
        this.radius = radius;
    }

    public double Area() {
        return PI * radius * radius;
    }
}

// Main class to test the shape classes
public class Q13 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the side length of the square: ");
        Square square = new Square(scanner.nextDouble());
        System.out.println("Area of the Square: " + square.Area());

        System.out.print("\nEnter the radius of the circle: ");
        Circle circle = new Circle(scanner.nextDouble());
        System.out.println("Area of the Circle: " + circle.Area());

        scanner.close();
    }
}
