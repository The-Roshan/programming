import java.util.Scanner;

public class Q2 {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("Simple Calculator");
            System.out.println("1. Addition (+)");
            System.out.println("2. Subtraction (-)");
            System.out.println("3. Multiplication (*)");
            System.out.println("4. Division (/)");
            System.out.println("5. Exponentiation (x^y)");
            System.out.println("6. Square Root (√x)");
            System.out.println("7. Exit");

            System.out.print("Choose an operation: ");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1: // Addition
                    double[] addNums = getTwoNumbers(scanner);
                    System.out.println("Result: " + (addNums[0] + addNums[1]));
                    break;

                case 2: // Subtraction
                    double[] subNums = getTwoNumbers(scanner);
                    System.out.println("Result: " + (subNums[0] - subNums[1]));
                    break;

                case 3: // Multiplication
                    double[] mulNums = getTwoNumbers(scanner);
                    System.out.println("Result: " + (mulNums[0] * mulNums[1]));
                    break;

                case 4: // Division
                    double[] divNums = getTwoNumbers(scanner);
                    if (divNums[1] != 0) {
                        System.out.println("Result: " + (divNums[0] / divNums[1]));
                    } else {
                        System.out.println("Error: Division by zero!");
                    }
                    break;

                case 5: // Exponentiation
                    System.out.print("Enter base number: ");
                    double base = scanner.nextDouble();
                    System.out.print("Enter exponent: ");
                    double exponent = scanner.nextDouble();
                    System.out.println("Result: " + Math.pow(base, exponent));
                    break;

                case 6: // Square Root
                    System.out.print("Enter number: ");
                    double sqrtNum = scanner.nextDouble();
                    if (sqrtNum >= 0) {
                        System.out.println("Result: " + Math.sqrt(sqrtNum));
                    } else {
                        System.out.println("Error: Cannot take square root of a negative number!");
                    }
                    break;

                case 7: // Exit
                    System.out.println("Exiting...");
                    scanner.close();
                    System.exit(0);
                    break;

                default:
                    System.out.println("Invalid choice! Please choose a valid operation.");
                    break;
            }

            System.out.println();
        }
    }

    // Helper function to input two numbers
    private static double[] getTwoNumbers(Scanner scanner) {
        double[] nums = new double[2];
        System.out.print("Enter first number: ");
        nums[0] = scanner.nextDouble();
        System.out.print("Enter second number: ");
        nums[1] = scanner.nextDouble();
        return nums;
    }
}
