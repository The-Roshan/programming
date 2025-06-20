#include <iostream>
#include <string>
using namespace std;
class Tour {
private:
int travel_id;
int no_of_adults;
int no_of_kids;
string source;
string destination;
float distance;
float total_fare;
public:
// Constructor to initialize all data members
Tour() : travel_id(0), no_of_adults(0), no_of_kids(0), source("NULL"), 
destination("NULL"), distance(0.0), total_fare(0.0) {}
// Function to calculate total fare
void calc_fare() {
float adult_fare, kid_fare;
if (distance >= 500)
adult_fare = 500;
else if (distance >= 300)
adult_fare = 300;
else
adult_fare = 150;
kid_fare = adult_fare * 0.5;
total_fare = (no_of_adults * adult_fare) + (no_of_kids * kid_fare);
}
// Function to read input data and calculate total fare
void read_data() {
cout << "Enter travel id: ";
cin >> travel_id;
cout << "Enter number of adults: ";
cin >> no_of_adults;
cout << "Enter number of kids: ";
cin >> no_of_kids;
cout << "Enter source: ";
cin >> source;
cout << "Enter destination: ";
cin >> destination;
cout << "Enter distance (in km): ";
cin >> distance;
calc_fare(); // Calculate total fare after reading data
}
// Function to display tour details
void show_data() {
cout << "Travel ID: " << travel_id << endl;
cout << "Number of adults: " << no_of_adults << endl;
cout << "Number of kids: " << no_of_kids << endl;
cout << "Source: " << source << endl;
cout << "Destination: " << destination << endl;
cout << "Distance: " << distance << " km" << endl;
cout << "Total Fare: Rs. " << total_fare << endl;
}
};
int main() {
Tour tour;
// Read tour data
tour.read_data();
// Display tour details
cout << "\nTour Details:\n";
tour.show_data();
return 0;
}
