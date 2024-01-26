#include <iostream>

std::string generateRandomPassword(int length) {
	const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=_+";
	const int charsetSize = std::strlen(charset);
	
	std::string password;
	password.reserve(length);

	srand(static_cast<unsigned int>(time(nullptr)));

	for (int i = 0; i < length; ++i) {
		password += charset[rand() % charsetSize];
	}

	return password;
}

int main() {
	int length;

	std::cout << "Enter the length of the password: ";
	std::cin >> length;

	if (length <= 0) {
		std::cerr << "Invalid input. Please enter a positive password length." << std::endl;
		return 1;
	}
	
    std::string password = generateRandomPassword(length);
	std::cout << "Generated Password:\n" << password;
}