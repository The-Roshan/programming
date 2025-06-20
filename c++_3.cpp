#include <iostream>
#include <cmath>
using namespace std;
bool isPerfect(int num)
{
    int sum = 1;
    for (int i = 2; i <= sqrt(num); i++)
    {
        if (num % i == 0)
        {
            if (num / i == i)
                sum = sum + i;
            else
                sum = sum + i + num / i;
        }
    }
    return sum == num;
}
bool isPalindrome(int num)
{
    int originalNum = num;
    int reversedNum = 0;
    while (num != 0)
    {
        int digit = num % 10;
        reversedNum = reversedNum * 10 + digit;
        num /= 10;
    }
    return originalNum == reversedNum;
}
bool isPrime(int num)
{
    if (num <= 1)
        return false;
    if (num == 2)
        return true;
    if (num % 2 == 0)
        return false;
    for (int i = 3; i <= sqrt(num); i += 2)
    {
        if (num % i == 0)
            return false;
    }
    return true;
}
int main()
{
    int choice;
    int num;
    while (true)
    {
        cout << "1. Check perfect number\n";
        cout << "2. Check palindrome number\n";
        cout << "3. Check prime number\n";
        cout << "4. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;
        if (choice == 4)
            break;
        cout << "Enter a number: ";
        cin >> num;
        switch (choice)
        {
        case 1:
            if (isPerfect(num))
                cout << num << " is a perfect number\n";
            else
                cout << num << " is not a perfect number\n";
            break;
        case 2:
            if (isPalindrome(num))
                cout << num << " is a palindrome number\n";
            else
                cout << num << " is not a palindrome number\n";
            break;
        case 3:
            if (isPrime(num))
                cout << num << " is a prime number\n";
            else
                cout << num << " is not a prime number\n";
            break;
        default:
            cout << "Invalid choice\n";
            break;
        }
    }
    return 0;
}
