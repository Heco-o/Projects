#include <iostream>
#include <ncurses.h>
#include <thread>
#include <unistd.h>
#include <sys/ioctl.h>
#include <vector>
#include <functional>
#include <csignal>
#include <atomic>
#include <chrono>
#include <mutex>
#include <string>
#include <random>

std::random_device rd;
std::mt19937 gen(rd());

int columns = -1, lines = -1;
std::atomic<bool> stopThread(false);
std::mutex stopThreadMutex;
std::mutex coordinatesMutex;

void signalHandler(int signal) {
	endwin();
	std::cout << "Received signal " << signal << ". Exiting..." << std::endl;
	{
		std::unique_lock<std::mutex> lock(stopThreadMutex);
		stopThread.store(true);
	}
	std::exit(signal);
}

bool getTerminalSize(int& columns, int& lines) {
	struct winsize ws;
	if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws) != -1) {
		columns = ws.ws_col - 1;
		lines = ws.ws_row;
		return true;
	} else {
		std::cerr << "Error retrieving terminal information." << std::endl;
		return false;
	}
}

void displayPosition(const std::vector<std::vector<char>>& coordinates) {
	while (!stopThread) {
		{
			std::unique_lock<std::mutex> lock(coordinatesMutex);
			clear();
			for (int i = 0; i < lines; i++) {
				for (int j = 0; j < columns; j++) {
					printw("%c", coordinates[i][j]);
				}
				printw("\n");
			}
			refresh();
		}
		std::this_thread::sleep_for(std::chrono::milliseconds(100));
	}
}

void inputThread(int& direction) {
	int ch;
	while (!stopThread && (ch = getch())) {
		switch (ch) {
			case 27:
				{
					std::unique_lock<std::mutex> lock(stopThreadMutex);
					stopThread.store(true);
				}
				break;
			case KEY_LEFT:
				break;
			case KEY_UP:
				direction = -1;
			case KEY_RIGHT:
				break;
			case KEY_DOWN:
				direction = 1;
		}
	}
}

struct Head {
	char base = '^';
	int direction = -1;
	int posX = columns / 2;
	int posY = lines / 2;
};

struct Body {
	char base = '#';
};

int main() {
	std::signal(SIGINT, signalHandler);
	std::signal(SIGQUIT, signalHandler);
	std::signal(SIGCONT, signalHandler);

	if (initscr() == NULL) {
		std::cerr << "Error initializing ncurses." << std::endl;
		return 1;
	}

	cbreak();
	keypad(stdscr, TRUE);

	if (!getTerminalSize(columns, lines)) {
		endwin();
		std::cerr << "Error retrieving terminal size." << std::endl;
		return 1;
	}

	std::vector<std::vector<char>> coordinates(lines, std::vector<char>(columns, ' '));
	std::vector<Body> bodies;

	Head head;
	coordinates[head.posY][head.posX] = head.base;

	std::thread display(displayPosition, std::ref(coordinates));
	std::thread input(inputThread, std::ref(head.direction));

	while (!stopThread) {
		{
			std::unique_lock<std::mutex> lock(coordinatesMutex);
			if ((head.posY == 0) && (head.direction == -1)) {
				coordinates[head.posY][head.posX] ^= coordinates[lines - 1][head.posX];
				coordinates[lines - 1][head.posX] ^= coordinates[head.posY][head.posX];
				coordinates[head.posY][head.posX] ^= coordinates[lines - 1][head.posX];

				head.posY = lines - 1;
				std::this_thread::sleep_for(std::chrono::milliseconds(100));
				continue;
			} else if (((head.posY + 1) == lines) && (head.direction == 1)) {
				coordinates[head.posY][head.posX] ^= coordinates[0][head.posX];
				coordinates[0][head.posX] ^= coordinates[head.posY][head.posX];
				coordinates[head.posY][head.posX] ^= coordinates[0][head.posX];

				head.posY = 0;
				std::this_thread::sleep_for(std::chrono::milliseconds(100));
				continue;
			}

			coordinates[head.posY][head.posX] ^= coordinates[head.posY + head.direction][head.posX];
			coordinates[head.posY + head.direction][head.posX] ^= coordinates[head.posY][head.posX];
			coordinates[head.posY][head.posX] ^= coordinates[head.posY + head.direction][head.posX];

			head.posY += head.direction;
		}

		std::this_thread::sleep_for(std::chrono::milliseconds(100));
	}

	display.join();
	input.join();
	endwin();
	std::cout << "Exited.." << std::endl;
	return 0;
}