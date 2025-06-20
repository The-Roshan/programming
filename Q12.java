//Create a class Account with two overloaded constructors. First constructor is used for initializing,
//name of account holder, account number and initial amount in account.
//Second constructor is used for initializing name of account holder, account number, addresses, type of account and current
//balance. Account class is having methods Deposit (), Withdraw (), and Get_Balance(). Make
//necessary assumption for data members and return types of the methods. Create objects of
//Account class and use them.

import java.util.Scanner;

class Account {
    private String accountHolderName, accountNumber, address, accountType;
    private double balance;

    public Account(String accountHolderName, String accountNumber, double initialAmount) {
        this.accountHolderName = accountHolderName;
        this.accountNumber = accountNumber;
        this.balance = initialAmount;
    }

    public Account(String accountHolderName, String accountNumber, String address, String accountType, double currentBalance) {
        this(accountHolderName, accountNumber, currentBalance);
        this.address = address;
        this.accountType = accountType;
    }

    public void deposit(double amount) { balance += amount; }
    public void withdraw(double amount) { if (amount <= balance) balance -= amount; }
    public double getBalance() { return balance; }

    public void displayAccountDetails() {
        System.out.println("Account Holder: " + accountHolderName);
        System.out.println("Account Number: " + accountNumber);
        if (address != null) System.out.println("Address: " + address);
        if (accountType != null) System.out.println("Account Type: " + accountType);
        System.out.println("Balance: " + balance);
    }
}

public class Q12 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter details for the first account:");
        System.out.print("Account Holder Name: ");
        String name1 = scanner.nextLine();
        System.out.print("Account Number: ");
        String number1 = scanner.nextLine();
        System.out.print("Initial Amount: ");
        double initialAmount1 = scanner.nextDouble();
        scanner.nextLine(); // consume newline
        Account account1 = new Account(name1, number1, initialAmount1);

        System.out.println("\nEnter details for the second account:");
        System.out.print("Account Holder Name: ");
        String name2 = scanner.nextLine();
        System.out.print("Account Number: ");
        String number2 = scanner.nextLine();
        System.out.print("Address: ");
        String address2 = scanner.nextLine();
        System.out.print("Account Type: ");
        String type2 = scanner.nextLine();
        System.out.print("Current Balance: ");
        double balance2 = scanner.nextDouble();
        scanner.nextLine(); // consume newline
        Account account2 = new Account(name2, number2, address2, type2, balance2);

        System.out.println("\nFirst Account Details:");
        account1.displayAccountDetails();

        System.out.println("\nSecond Account Details:");
        account2.displayAccountDetails();

        System.out.print("\nEnter amount to deposit in first account: ");
        account1.deposit(scanner.nextDouble());

        System.out.print("Enter amount to withdraw from first account: ");
        account1.withdraw(scanner.nextDouble());

        System.out.print("\nEnter amount to deposit in second account: ");
        account2.deposit(scanner.nextDouble());

        System.out.print("Enter amount to withdraw from second account: ");
        account2.withdraw(scanner.nextDouble());

        System.out.println("\nFinal Balance of First Account: " + account1.getBalance());
        System.out.println("Final Balance of Second Account: " + account2.getBalance());

        scanner.close();
    }
}
