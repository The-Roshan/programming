import java.util.Scanner;

public class Q9 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Rows of matrix 1: ");
        int r1 = sc.nextInt();
        System.out.print("Cols of matrix 1: ");
        int c1 = sc.nextInt();
        System.out.print("Rows of matrix 2: ");
        int r2 = sc.nextInt();
        System.out.print("Cols of matrix 2: ");
        int c2 = sc.nextInt();

        if (c1 != r2) {
            System.out.println("Multiplication not possible.");
        } else {
            int[][] m1 = new int[r1][c1];
            int[][] m2 = new int[r2][c2];
            int[][] product = new int[r1][c2];

            System.out.println("Enter elements of matrix 1:");
            for (int i = 0; i < r1; i++)
                for (int j = 0; j < c1; j++)
                    m1[i][j] = sc.nextInt();

            System.out.println("Enter elements of matrix 2:");
            for (int i = 0; i < r2; i++)
                for (int j = 0; j < c2; j++)
                    m2[i][j] = sc.nextInt();

            for (int i = 0; i < r1; i++)
                for (int j = 0; j < c2; j++)
                    for (int k = 0; k < c1; k++)
                        product[i][j] += m1[i][k] * m2[k][j];

            System.out.println("Product of matrices:");
            for (int[] row : product) {
                for (int val : row) System.out.print(val + " ");
                System.out.println();
            }
        }

        sc.close();
    }
}
