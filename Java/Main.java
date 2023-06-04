import java.util.Scanner;
public class Main {
	public static void main(String[] args) {
		Scanner input = new Scanner(System.in);
		System.out.println("Please enter the number");
		long number = input.nextLong();
		long step = 0;
		long highest = 0;
		do {
			if (number % 2 == 0) {
				number /= 2;
			} else {
				number = number * 3 + 1;
			}
			if (number > highest) {
				highest = number;
			}
			step++;
			System.out.print(number + " ");
		} while (number != 1 && number > 0);
		System.out.println("\nTotal " + step + " steps");
		System.out.print("The highest number was " + highest);
		input.close();
	}
}