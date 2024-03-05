#include <iostream>
#include <limits>

int main() {
	std::cout << "Integer Limits:" << std::endl;
	std::cout << "---------------------" << std::endl;
	std::cout << "char: " << std::numeric_limits<char>::min() << " to " << std::numeric_limits<char>::max() << std::endl;
	std::cout << "short: " << std::numeric_limits<short>::min() << " to " << std::numeric_limits<short>::max() << std::endl;
	std::cout << "int: " << std::numeric_limits<int>::min() << " to " << std::numeric_limits<int>::max() << std::endl;
	std::cout << "long: " << std::numeric_limits<long>::min() << " to " << std::numeric_limits<long>::max() << std::endl;
	std::cout << "long long: " << std::numeric_limits<long long>::min() << " to " << std::numeric_limits<long long>::max() << std::endl;

	std::cout << "\nFloating Point Limits:" << std::endl;
	std::cout << "---------------------" << std::endl;
	std::cout << "float: " << std::numeric_limits<float>::min() << " to " << std::numeric_limits<float>::max() << std::endl;
	std::cout << "double: " << std::numeric_limits<double>::min() << " to " << std::numeric_limits<double>::max() << std::endl;
	std::cout << "long double: " << std::numeric_limits<long double>::min() << " to " << std::numeric_limits<long double>::max() << std::endl;

	std::cout << "\nOther Limits:" << std::endl;
	std::cout << "---------------------" << std::endl;
	std::cout << "bool: " << std::numeric_limits<bool>::min() << " to " << std::numeric_limits<bool>::max() << std::endl;
	std::cout << "wchar_t: " << std::numeric_limits<wchar_t>::min() << " to " << std::numeric_limits<wchar_t>::max() << std::endl;

	return 0;
}
