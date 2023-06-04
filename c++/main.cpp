#include <iostream>
#include <math.h>
int main(int argc, char* argv[]) {
	long double number = std::atof(argv[1]);
	long double step;
	long double highest;
	do {
		if(fmod(number, 2.0) == 0) {
			number /= 2.0;
		}
		else {
			number = 3.0 * number + 1.0;
		}
		if(number > highest) {
			highest = number;
		}
		step++;
		std::cout << number << " ";
	} while(number != 1.0);
	std::cout << std::endl << "Total " << step << " step" << std::endl;
	std::cout << "The highest number was " << highest << std::endl;
}