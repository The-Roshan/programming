#include <iostream>
using namespace std;

void displayFibonacci(int n) {
    int a = 0, b = 1;
    cout << "Fibonacci Series up to " << n << " terms: ";
    for (int i = 0; i < n; ++i) {
        cout << a << " ";
        int temp = a + b;
        a = b;
        b = temp;
    }
}

int main() {
    int n;
    cout << "Enter the number of terms: ";
    cin >> n;
    displayFibonacci(n);
    return 0;
}
