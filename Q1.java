//Q. write a program to input and display different types of data values using scanner and stream class.

import java.util.Scanner;

class Q1 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("Different data values:");
        System.out.println("Enter a integer value: ");
        int a = sc.nextInt();
        System.out.println("Enter a float value: ");
        float b = sc.nextFloat();
        System.out.println("Enter a double value: ");
        double c=sc.nextDouble();

        System.out.println(a);
        System.out.println(b);
        System.out.println(c);
    }
}