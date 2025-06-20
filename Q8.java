import java.util.Arrays;
import java.util.Scanner;

public class Q8 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Number of elements: ");
        int n = sc.nextInt();
        int[] arr = new int[n];

        System.out.println("Enter elements:");
        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();

        if (isSorted(arr)) {
            System.out.println(isAscending(arr) ? "Sorted in ascending order." : "Sorted in descending order.");
        } else {
            System.out.print("1 for ascending, 2 for descending: ");
            int choice = sc.nextInt();
            Arrays.sort(arr);
            if (choice == 2) reverse(arr);
            System.out.println("Sorted array: " + Arrays.toString(arr));
        }
        sc.close();
    }

    static boolean isSorted(int[] arr) {
        return isAscending(arr) || isDescending(arr);
    }

    static boolean isAscending(int[] arr) {
        for (int i = 1; i < arr.length; i++) if (arr[i] < arr[i - 1]) return false;
        return true;
    }

    static boolean isDescending(int[] arr) {
        for (int i = 1; i < arr.length; i++) if (arr[i] > arr[i - 1]) return false;
        return true;
    }

    static void reverse(int[] arr) {
        for (int i = 0, j = arr.length - 1; i < j; i++, j--) {
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
}
