//Write a program to input a string and display number of vowels and consonant in each word.
//For example, if the string is “Kolhan University Chaibasa”, then the output will be –
//Kolhan: Vowels = 2, Consonants = 4
//University: Vowels = 4, Consonants = 6
//Chaibasa: Vowels = 4, Consonants = 4

import java.util.Scanner;

public class Q10 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Input the string
        System.out.print("Enter a string: ");
        String input = scanner.nextLine();

        // Split the string into words
        String[] words = input.split("\\s+");

        // Process each word
        for (String word : words) {
            int vowelCount = 0;
            int consonantCount = 0;

            // Convert word to lowercase for easier comparison
            word = word.toLowerCase();

            // Count vowels and consonants
            for (int i = 0; i < word.length(); i++) {
                char ch = word.charAt(i);
                if (isVowel(ch)) {
                    vowelCount++;
                } else if (isConsonant(ch)) {
                    consonantCount++;
                }
            }

            // Display the result for the word
            System.out.println(word.substring(0, 1).toUpperCase() + word.substring(1) + ": Vowels = " + vowelCount + ", Consonants = " + consonantCount);
        }

        scanner.close();
    }

    // Method to check if a character is a vowel
    public static boolean isVowel(char ch) {
        return "aeiou".indexOf(ch) != -1;
    }

    // Method to check if a character is a consonant
    public static boolean isConsonant(char ch) {
        return ch >= 'a' && ch <= 'z' && !isVowel(ch);
    }
}
