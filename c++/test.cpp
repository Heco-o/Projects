#include <iostream>

int main() {
    const int rows = 20;
    const int cols = 20;

    char array[rows][cols];
	for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            array[i][j] = ' ';
        }
    }
    // Assume array is initialized with some values
	array[12][5] = 'E';
	array[13][5] = '#';
    // Swap values between array[12][5] and array[13][5] without a temporary variable
    array[12][5] ^= array[13][5];
    array[13][5] ^= array[12][5];
    array[12][5] ^= array[13][5];

    // Display the updated array
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            std::cout << array[i][j] << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}