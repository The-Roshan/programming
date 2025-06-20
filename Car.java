// Define the first interface
interface Vehicle {
    void drive();
}

// Define the second interface
interface Machine {
    void operate();
}

// A class can implement multiple interfaces
public class Car implements Vehicle, Machine {
    public void drive() {
        System.out.println("Car is driving.");
    }

    public void operate() {
        System.out.println("Car's machine is operating.");
    }

    public static void main(String[] args) {
        Car car = new Car();
        car.drive();
        car.operate();
    }
}