//Write a program to input length of three sides of a triangle. Then check if these sides will form a triangle or not. If sides form a triangle, then display the type of the triangle with its area and
//perimeter

import java.util.Scanner;

public class Q4 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Input the lengths of the three sides of the triangle
        System.out.print("Enter the length of side 1: ");
        double side1 = scanner.nextDouble();
        System.out.print("Enter the length of side 2: ");
        double side2 = scanner.nextDouble();
        System.out.print("Enter the length of side 3: ");
        double side3 = scanner.nextDouble();

        // Check if the sides form a valid triangle
        if (isTriangleValid(side1, side2, side3)) {
            System.out.println("The sides form a valid triangle.");

            // Determine the type of the triangle
            String triangleType = determineTriangleType(side1, side2, side3);
            System.out.println("Type of the triangle: " + triangleType);

            // Calculate the perimeter of the triangle
            double perimeter = calculatePerimeter(side1, side2, side3);
            System.out.println("Perimeter of the triangle: " + perimeter);

            // Calculate the area of the triangle
            double area = calculateArea(side1, side2, side3);
            System.out.println("Area of the triangle: " + area);
        } else {
            System.out.println("The sides do not form a valid triangle.");
        }

        scanner.close();
    }

    // Method to check if the sides can form a valid triangle
    public static boolean isTriangleValid(double a, double b, double c) {
        return (a + b > c) && (b + c > a) && (c + a > b);
    }

    // Method to determine the type of the triangle
    public static String determineTriangleType(double a, double b, double c) {
        if (a == b && b == c) {
            return "Equilateral";
        } else if (a == b || b == c || c == a) {
            return "Isosceles";
        } else {
            return "Scalene";
        }
    }

    // Method to calculate the perimeter of the triangle
    public static double calculatePerimeter(double a, double b, double c) {
        return a + b + c;
    }

    // Method to calculate the area of the triangle using Heron's formula
    public static double calculateArea(double a, double b, double c) {
        double s = (a + b + c) / 2; // semi-perimeter
        return Math.sqrt(s * (s - a) * (s - b) * (s - c));
    }
}
