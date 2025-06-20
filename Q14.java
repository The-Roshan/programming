//Define an Employee class with suitable attributes having getSalary() method, which returns salary
//withdrawn by a particular employee. Write a class Manager which extends a class Employee,
//override the getSalary() method, which will return salary of manager by adding traveling
//_allowance, house rent allowance etc. Use default and parameterized constructors to initialize
//data.

class Employee {
    private double salary;

//    public Employee() {
//        this.salary = 0;
//    }

    public Employee(double salary) {
        this.salary = salary;
    }

    public double getSalary() {
        return salary;
    }
}

class Manager extends Employee {
    private double travelAllowance, houseRentAllowance;

//    public Manager() {
//        super(0);
//        this.travelAllowance = 0;
//        this.houseRentAllowance = 0;
//    }

    public Manager(double salary, double travelAllowance, double houseRentAllowance) {
        super(salary);
        this.travelAllowance = travelAllowance;
        this.houseRentAllowance = houseRentAllowance;
    }

    @Override
    public double getSalary() {
        return super.getSalary() + travelAllowance + houseRentAllowance;
    }

    public double getPreviousSalary() {
        return super.getSalary();
    }

    public double getTravelAllowance() {
        return travelAllowance;
    }

    public double getHouseRentAllowance() {
        return houseRentAllowance;
    }
}

public class Q14 {
    public static void main(String[] args) {
        Employee employee = new Employee(40000);
        Manager manager = new Manager(50000, 5000, 8000);

        System.out.println("Employee Salary Details:");
        System.out.println("Employee Salary: " + employee.getSalary());

        System.out.println("Manager Salary Details:");
        System.out.println("Manager Basic Salary: " + manager.getPreviousSalary());
        System.out.println("Travel Allowance: " + manager.getTravelAllowance());
        System.out.println("House Rent Allowance: " + manager.getHouseRentAllowance());
        System.out.println("Total Salary of Manager: " + manager.getSalary());
    }
}
