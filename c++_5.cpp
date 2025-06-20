#include <iostream>
#include <vector>
using namespace std;
// Function to perform matrix addition
vector<vector<int>> matrixAddition(const vector<vector<int>>& matrix1, const vector<vector<int>>& 
matrix2) {
int rows1 = matrix1.size();
int cols1 = matrix1[0].size();
int rows2 = matrix2.size();
int cols2 = matrix2[0].size();
// Check if the matrices have the same order
if (rows1 != rows2 || cols1 != cols2) {
cout << "Matrices cannot be added as they don't have the same order." << endl;
return {};
}
// Initialize result matrix with size same as input matrices
vector<vector<int>> result(rows1, vector<int>(cols1));
// Perform addition
for (int i = 0; i < rows1; ++i) {
for (int j = 0; j < cols1; ++j) {
result[i][j] = matrix1[i][j] + matrix2[i][j];
}
}
return result;
}
int main() {
int rows, cols;
// Input order of first matrix
cout << "Enter the number of rows and columns of the matrices: ";
cin >> rows >> cols;
// Input elements of first matrix
cout << "Enter elements of first matrix:" << endl;
 
vector<vector<int>> matrix1(rows, vector<int>(cols));
for (int i = 0; i < rows; ++i) {
for (int j = 0; j < cols; ++j) {
cin >> matrix1[i][j];
}
}
// Input elements of second matrix
cout << "Enter elements of second matrix:" << endl;
vector<vector<int>> matrix2(rows, vector<int>(cols));
for (int i = 0; i < rows; ++i) {
for (int j = 0; j < cols; ++j) {
cin >> matrix2[i][j];
}
}
// Perform addition and display result
vector<vector<int>> sum = matrixAddition(matrix1, matrix2);
if (!sum.empty()) {
cout << "Sum of the matrices:" << endl;
for (const auto& row : sum) {
for (int element : row) {
cout << element << " ";
}
cout << endl;
}
}
return 0;
}
