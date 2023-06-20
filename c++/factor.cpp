#include <iostream>
#include <math.h>
#include <vector>
#include <iomanip>
int main(int argc, char* argv[]) {
	long double number = std::atof(argv[1]);
	long double divisor = 1;
	long double total = 0;
	std::vector < long double > results;
	while(divisor * divisor <= number) {
		if(fmod(number, divisor) == 0) {
			results.push_back(divisor);
			if(number / divisor != divisor) {
				results.push_back(number / divisor);
			};
		};
		divisor++;
	};
	std::sort(results.begin(), results.end());
	for(auto& i: results) {
		total += i;
		std::cout << std::fixed << std::setprecision(0) << i << " ";
	};
	std::cout << "\n\nSum of its divisors: " << total;
	std::cout << "\nNumber of divisors: " << results.size();
};