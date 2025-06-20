import java.util.Scanner;

public class Q7 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int choice;
        do {
            System.out.println("\nMenu:");
            System.out.println("1. Convert Decimal to Binary");
            System.out.println("2. Convert Binary to Decimal");
            System.out.println("3. Exit");
            System.out.print("Enter your choice (1-3): ");
            choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter a decimal number: ");
                    int decimalNumber = scanner.nextInt();
                    System.out.println("Binary equivalent: " + Integer.toBinaryString(decimalNumber));
                    break;
                case 2:
                    System.out.print("Enter a binary number: ");
                    String binaryNumber = scanner.next();
                    System.out.println("Decimal equivalent: " + Integer.parseInt(binaryNumber, 2));
                    break;
                case 3:
                    System.out.println("Exiting the program...");
                    break;
                default:
                    System.out.println("Invalid choice! Try again");
                    break;
            }
        } while (choice != 3);

        scanner.close();
    }
}
