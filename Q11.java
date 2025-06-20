import java.util.Scanner;

class Rectangle {
    double width, length, area;
    String color;

    void setLength(double length) { this.length = length; }
    void setWidth(double width) { this.width = width; }
    void setColor(String color) { this.color = color; }
    void findArea() { this.area = this.length * this.width; }
}

public class Q11 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Rectangle rect1 = new Rectangle();
        Rectangle rect2 = new Rectangle();

        System.out.print("Enter length, width, and color for the first rectangle: ");
        rect1.setLength(sc.nextDouble());
        rect1.setWidth(sc.nextDouble());
        sc.nextLine();  // Consume newline
        rect1.setColor(sc.nextLine());
        rect1.findArea();

        System.out.print("Enter length, width, and color for the second rectangle: ");
        rect2.setLength(sc.nextDouble());
        rect2.setWidth(sc.nextDouble());
        sc.nextLine();  // Consume newline
        rect2.setColor(sc.nextLine());
        rect2.findArea();

        String result = (rect1.area == rect2.area && rect1.color.equalsIgnoreCase(rect2.color)) ? "Matching Rectangles" : "Non-matching Rectangles";
        System.out.println(result);

        sc.close();
    }
}
