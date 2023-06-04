#include <iostream>

int main() {
	for(long double n = 1; n < n + 1; n++) {
		long double a = 2;
		long double b = 2;
		long double c = 2;
		long double d = 2;
		long double result = a + b * (n - 1) + (c * (n - 1) * (n - 2)) / 2 + (d * (n - 1) * (n - 2) * (n - 3)) / 6;
		std::cout << result << std::endl;
	}
}