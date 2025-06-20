//Write a program to convert primitive to wrapper class and wrapper to primitive.

public class Q3 {
    public static void main(String[] args) {
        // Primitive to Wrapper Conversion (Boxing)
        int primitiveInt = 5;
        Integer wrapperInt = Integer.valueOf(primitiveInt); // explicit boxing
        Integer autoBoxedInt = primitiveInt; // auto-boxing (automatic)

        System.out.println("Primitive int: " + primitiveInt);
        System.out.println("Wrapper Integer (Boxed): " + wrapperInt);
        System.out.println("Wrapper Integer (Auto-boxed): " + autoBoxedInt);

        // Wrapper to Primitive Conversion (Unboxing)
        Integer anotherWrapperInt = new Integer(10);
        int unboxedInt = anotherWrapperInt.intValue(); // explicit unboxing
        int autoUnboxedInt = anotherWrapperInt; // auto-unboxing (automatic)

        System.out.println("Wrapper Integer: " + anotherWrapperInt);
        System.out.println("Primitive int (Unboxed): " + unboxedInt);
        System.out.println("Primitive int (Auto-unboxed): " + autoUnboxedInt);
    }
}
