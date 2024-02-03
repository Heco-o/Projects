#include <iostream>
#include <ncurses.h>
#include <thread>
#include <csignal>
#include <chrono>

std::string text;

void signalHandler(int signal) {
	endwin();
	std::cout << "exited.." << std::endl;
	std::exit(signal);
}

void print() {
	clear(); // Clear the screen before printing
	printw("%s\n", text.c_str());
	refresh(); // Refresh the screen to display the printed text
}

void inputThread() {
	int ch;
	while ((ch = getch())) {
		switch (ch) {
			case KEY_UP:
				text = "Up";
				break;
			case KEY_DOWN:
				text = "Down";
				break;
			case 'q':
				std::raise(SIGINT); // Raise SIGINT to gracefully exit the program
				break;
		}
		print();
	}
}

int main() {
	std::signal(SIGINT, signalHandler);

	// Initialize ncurses
	initscr();
	cbreak();
	keypad(stdscr, TRUE);

	// Create a thread for user input
	std::thread input(inputThread);

	// Wait for user input with a sleep to reduce CPU usage
	while (true) {
		std::this_thread::sleep_for(std::chrono::milliseconds(100));
	}

	// Wait for the input thread to finish
	input.join();

	// Clean up ncurses and exit
	endwin();
	return 0;
}