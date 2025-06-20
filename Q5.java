//Write a program to find factorial of a number. Input the number as command line argument.

public class Q5 {
    public static void main(String[] args) {
        // Check if exactly one command-line argument is provided
        if (args.length != 1) {
            System.out.println("Please provide a single integer as a command-line argument.");
            return;
        }

        try {
            // Parse the command-line argument to an integer
            int number = Integer.parseInt(args[0]);

            // Check if the number is non-negative
            if (number < 0) {
                System.out.println("Factorial is not defined for negative numbers.");
            } else {
                // Calculate the factorial
                long factorial = calculateFactorial(number);
                System.out.println("The factorial of " + number + " is: " + factorial);
            }
        } catch (NumberFormatException e) {
            System.out.println("Please provide a valid integer.");
        }
    }

    // Method to calculate the factorial of a number
    public static long calculateFactorial(int n) {
        long result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }
}

//output

//javac Q5.java
//java Q5 5
//The factorial of 5 is: 120
