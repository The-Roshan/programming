//Write a menu-based program to check Prime, Armstrong, and Perfect number.

import java.util.Scanner;

public class Q6 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int choice;

        do {
            // Display menu
            System.out.println("\nMenu:");
            System.out.println("1. Check Prime Number");
            System.out.println("2. Check Armstrong Number");
            System.out.println("3. Check Perfect Number");
            System.out.println("4. Exit");
            System.out.print("Enter your choice (1-4): ");
            choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter a number to check if it's Prime: ");
                    int primeNumber = scanner.nextInt();
                    if (isPrime(primeNumber)) {
                        System.out.println(primeNumber + " is a Prime number.");
                    } else {
                        System.out.println(primeNumber + " is not a Prime number.");
                    }
                    break;

                case 2:
                    System.out.print("Enter a number to check if it's Armstrong: ");
                    int armstrongNumber = scanner.nextInt();
                    if (isArmstrong(armstrongNumber)) {
                        System.out.println(armstrongNumber + " is an Armstrong number.");
                    } else {
                        System.out.println(armstrongNumber + " is not an Armstrong number.");
                    }
                    break;

                case 3:
                    System.out.print("Enter a number to check if it's Perfect: ");
                    int perfectNumber = scanner.nextInt();
                    if (isPerfect(perfectNumber)) {
                        System.out.println(perfectNumber + " is a Perfect number.");
                    } else {
                        System.out.println(perfectNumber + " is not a Perfect number.");
                    }
                    break;

                case 4:
                    System.out.println("Exiting the program...");
                    break;

                default:
                    System.out.println("Invalid choice! Please select a valid option.");
                    break;
            }
        } while (choice != 4);

        scanner.close();
    }

    // Method to check if a number is Prime
    public static boolean isPrime(int num) {
        if (num <= 1) return false;
        for (int i = 2; i <= Math.sqrt(num); i++) {
            if (num % i == 0) return false;
        }
        return true;
    }

    // Method to check if a number is Armstrong
    public static boolean isArmstrong(int num) {
        int originalNumber = num, remainder, result = 0;
        int n = 0;

        // Find the number of digits in the number
        while (originalNumber != 0) {
            originalNumber /= 10;
            n++;
        }

        originalNumber = num;

        // Calculate the sum of the power of digits
        while (originalNumber != 0) {
            remainder = originalNumber % 10;
            result += Math.pow(remainder, n);
            originalNumber /= 10;
        }

        return result == num;
    }

    // Method to check if a number is Perfect
    public static boolean isPerfect(int num) {
        int sum = 1;
        for (int i = 2; i <= num / 2; i++) {
            if (num % i == 0) sum += i;
        }
        return sum == num && num != 1;
    }
}
