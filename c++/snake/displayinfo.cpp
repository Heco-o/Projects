#include <iostream>
#include <unistd.h>
#include <sys/ioctl.h>

void getTerminalSize(int& columns, int& lines) {
	struct winsize ws;
	if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws) != -1) {
		columns = ws.ws_col;
		lines = ws.ws_row;
	} else {
		std::cerr << "Error retrieving terminal information." << std::endl;
		columns = -1;
		lines = -1;
	}
}

int main() {
	int columns, lines;
	getTerminalSize(columns, lines);

	if (columns != -1 && lines != -1) {
		std::cout << "Terminal columns: " << columns << std::endl;
		std::cout << "Terminal lines: " << lines << std::endl;
	}

	return 0;
}