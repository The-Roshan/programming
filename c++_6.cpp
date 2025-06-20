#include <iostream>
using namespace std;
int main()
{
// Input string
cout << "Enter a string: ";
string str;
cin >> str;
// Finding reverse of the string
string reverse_str;
for (int i = str.length() - 1; i >= 0; --i)
{
reverse_str += str[i];
}
// Checking if the string is a palindrome
bool is_palindrome = true;
for (int i = 0; i < str.length(); ++i)
{
if (str[i] != reverse_str[i])
{
is_palindrome = false;
break;
}
}
// Output
if (is_palindrome)
{
cout << "The string \"" << str << "\" is a palindrome.\n";
}
else
{
cout << "The string \"" << str << "\" is not a palindrome.\n";
}
return 0;
}
