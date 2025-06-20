#include <iostream>
using namespace std;
int main() {
int n;
// Input the number of elements
cout << "Enter the number of elements (N): ";
cin >> n;
if (n <= 0) {
cout << "Invalid input. Exiting program.\n";
return 1;
}
// Dynamically allocate an array of size N
int *arr = new int[n];
// Input the array elements
cout << "Enter " << n << " integer elements:\n";
for (int i = 0; i < n; ++i) {
cout << "Element " << i + 1 << ": ";
cin >> arr[i];
}
// Find the index of the largest and lowest elements
int maxIndex = 0, minIndex = 0;
for (int i = 1; i < n; ++i) {
if (arr[i] > arr[maxIndex]) {
maxIndex = i;
}
if (arr[i] < arr[minIndex]) {
minIndex = i;
}
}
// Swap the largest and lowest elements
int temp = arr[maxIndex];
arr[maxIndex] = arr[minIndex];
arr[minIndex] = temp;
// Display the modified array
 
cout << "Array after swapping the largest and lowest elements:\n";
for (int i = 0; i < n; ++i) {
cout << arr[i] << " ";
}
// Deallocate the dynamically allocated array
delete[] arr;
return 0;
}
