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

/*
#include <stdio.h>
FILE *logFile;
void writeToLog(const char *format, ...) {
	if (logFile == NULL) {
		logFile = fopen("logfile.txt", "a");
		if (logFile == NULL) {
			printf("Error opening log file.\n");
			return;
		}
	}

	va_list args;
	va_start(args, format);
	vfprintf(logFile, format, args);
	va_end(args);
	fflush(logFile);
	fclose(logFile);
	logFile = NULL;
}
*/

struct Head {
	char base;
	char bases[4] = {'^', 'v', '<', '>'};
	int directionX = 0;
	int directionY = -1;
	int pastX, pastY, posX, posY;
};

struct Body {
	char base = '#';
	int directionX, directionY, pastX, pastY, posX, posY;
};

struct Food{
	char base = '@';
	int posX, posY;
};

std::random_device rd;
std::mt19937 gen(rd());

int columns = -1, lines = -1, score;
bool foodCreation, gameOver;
std::atomic<bool> stopThread(false);
Head head; Food food; Body tempBody;
std::vector<Body> bodies;
std::mutex stopThreadMutex;
std::mutex coordinatesMutex;
std::mutex headMutex;

void signalHandler(int signal) {
	endwin();
	std::cout << "Received signal " << signal << ". Exiting..." << std::endl;
	{
		std::unique_lock<std::mutex> lock0(stopThreadMutex);
		stopThread.store(true);
	}
	std::exit(signal);
}

bool getTerminalSize(int& columns, int& lines) {
	struct winsize ws;
	if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws) != -1) {
		columns = ws.ws_col - 1;
		lines = ws.ws_row - 1;
		return true;
	} else {
		std::cerr << "Error retrieving terminal information." << std::endl;
		return false;
	}
}

void displayPosition(const std::vector<std::vector<char>>& coordinates) {
	while (!stopThread) {
		{
			std::unique_lock<std::mutex> lock1(coordinatesMutex);
			clear();
			for (int i = 0; i < lines; i++) {
				for (int j = 0; j < columns; j++) {
					printw("%c", coordinates[i][j]);
				}
				printw("\n");
			}
			printw("score: %d", score);
			refresh();
		}
		std::this_thread::sleep_for(std::chrono::milliseconds(10));
	}
}

void inputThread() {
	int ch;
	while (!stopThread && (ch = getch())) {
		{
			std::unique_lock<std::mutex> lock2(headMutex);
			
			switch (ch) {
				case 27:
					{
						std::unique_lock<std::mutex> lock0(stopThreadMutex);
						stopThread.store(true);
					}
					break;
				case KEY_LEFT:
					if (head.directionX != 1){
						head.directionX = -1;
						head.directionY = 0;
					}
					break;
				case KEY_UP:
					if (head.directionY != 1){
						head.directionX = 0;
						head.directionY = -1;
					}
					break;
				case KEY_RIGHT:
					if (head.directionX != -1){
						head.directionX = 1;
						head.directionY = 0;
					}
					break;
				case KEY_DOWN:
					if (head.directionY != -1){
						head.directionX = 0;
						head.directionY = 1;
					}
					break;
			}
		}
	}
}

void next(std::vector<std::vector<char>>& coordinates){
	if (bodies.size() > 0){
		//writeToLog("%d\n", head.pastX);
		//writeToLog("%d\n", head.pastY);
		if (head.pastY == 0){
			if ((bodies[0].posX == 0) && (head.pastX == -1)) {
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[bodies[0].posY][columns - 1];
				coordinates[bodies[0].posY][columns - 1] ^= coordinates[bodies[0].posY][bodies[0].posX];
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[bodies[0].posY][columns - 1];
				
				bodies[0].posX = columns - 1;
			} else if (((bodies[0].posX + 1) == columns) && (head.pastX == 1)) {
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[bodies[0].posY][0];
				coordinates[bodies[0].posY][0] ^= coordinates[bodies[0].posY][bodies[0].posX];
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[bodies[0].posY][0];
				
				bodies[0].posX = 0;
			} else{
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[bodies[0].posY][bodies[0].posX + head.pastX];
				coordinates[bodies[0].posY][bodies[0].posX + head.pastX] ^= coordinates[bodies[0].posY][bodies[0].posX];
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[bodies[0].posY][bodies[0].posX + head.pastX];
				
				bodies[0].posX += head.pastX;
			}
		} else if (head.pastX == 0){
			if ((bodies[0].posY == 0) && (head.pastY == -1)) {
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[lines - 1][bodies[0].posX];
				coordinates[lines - 1][bodies[0].posX] ^= coordinates[bodies[0].posY][bodies[0].posX];
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[lines - 1][bodies[0].posX];
				
				bodies[0].posY = lines - 1;
			} else if (((bodies[0].posY + 1) == lines) && (head.pastY == 1)) {
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[0][bodies[0].posX];
				coordinates[0][bodies[0].posX] ^= coordinates[bodies[0].posY][bodies[0].posX];
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[0][bodies[0].posX];
				
				bodies[0].posY = 0;
			} else{
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[bodies[0].posY + head.pastY][bodies[0].posX];
				coordinates[bodies[0].posY + head.pastY][bodies[0].posX] ^= coordinates[bodies[0].posY][bodies[0].posX];
				coordinates[bodies[0].posY][bodies[0].posX] ^= coordinates[bodies[0].posY + head.pastY][bodies[0].posX];
				
				bodies[0].posY += head.pastY;
			}
		}
		bodies[0].pastX = bodies[0].directionX;
		bodies[0].pastY = bodies[0].directionY;
		bodies[0].directionX = head.pastX;
		bodies[0].directionY = head.pastY;
	}
	for (int i = 1; i < bodies.size(); i++){
		if (bodies[i - 1].pastY == 0){
			if ((bodies[i].posX == 0) && (bodies[i - 1].pastX == -1)) {
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[bodies[i].posY][columns - 1];
				coordinates[bodies[i].posY][columns - 1] ^= coordinates[bodies[i].posY][bodies[i].posX];
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[bodies[i].posY][columns - 1];
				
				bodies[i].posX = columns - 1;
			} else if (((bodies[i].posX + 1) == columns) && (bodies[i - 1].pastX == 1)) {
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[bodies[i].posY][0];
				coordinates[bodies[i].posY][0] ^= coordinates[bodies[i].posY][bodies[i].posX];
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[bodies[i].posY][0];
				
				bodies[i].posX = 0;
			} else{
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[bodies[i].posY][bodies[i].posX + bodies[i - 1].pastX];
				coordinates[bodies[i].posY][bodies[i].posX + bodies[i - 1].pastX] ^= coordinates[bodies[i].posY][bodies[i].posX];
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[bodies[i].posY][bodies[i].posX + bodies[i - 1].pastX];
				
				bodies[i].posX += bodies[i - 1].pastX;
			}
		} else if (bodies[i - 1].pastX == 0){
			if ((bodies[i].posY == 0) && (bodies[i - 1].pastY == -1)) {
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[lines - 1][bodies[i].posX];
				coordinates[lines - 1][bodies[i].posX] ^= coordinates[bodies[i].posY][bodies[i].posX];
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[lines - 1][bodies[i].posX];
				
				bodies[i].posY = lines - 1;
			} else if (((bodies[i].posY + 1) == lines) && (bodies[i - 1].pastY == 1)) {
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[0][bodies[i].posX];
				coordinates[0][bodies[i].posX] ^= coordinates[bodies[i].posY][bodies[i].posX];
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[0][bodies[i].posX];
				
				bodies[i].posY = 0;
			} else{
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[bodies[i].posY + bodies[i - 1].pastY][bodies[i].posX];
				coordinates[bodies[i].posY + bodies[i - 1].pastY][bodies[i].posX] ^= coordinates[bodies[i].posY][bodies[i].posX];
				coordinates[bodies[i].posY][bodies[i].posX] ^= coordinates[bodies[i].posY + bodies[i - 1].pastY][bodies[i].posX];
				
				bodies[i].posY += bodies[i - 1].pastY;
			}
		}
		bodies[i].pastX = bodies[i].directionX;
		bodies[i].pastY = bodies[i].directionY;
		bodies[i].directionX = bodies[i - 1].pastX;
		bodies[i].directionY = bodies[i - 1].pastY;
	}
	head.pastX = head.directionX;
	head.pastY = head.directionY;
}

void generateBody(std::vector<std::vector<char>>& coordinates){
	if (bodies.size() < 1){
		Body body;
		body.directionX = head.pastX;
		body.directionY = head.pastY;
		body.posX = head.posX - head.directionX;
		body.posY = head.posY - head.directionY;
		coordinates[body.posY][body.posX] = body.base;
		
		bodies.push_back(body);
	} else{
		int currentSize = bodies.size() - 1;
		Body body;
		body.directionX = bodies[currentSize].pastX;
		body.directionY = bodies[currentSize].pastY;
		body.posX = bodies[currentSize].posX - bodies[currentSize].directionX;
		body.posY = bodies[currentSize].posY - bodies[currentSize].directionY;
		coordinates[body.posY][body.posX] = body.base;
		
		bodies.push_back(body);
	}
}

void generateFood(std::uniform_int_distribution<int>& distributionX, std::uniform_int_distribution<int>& distributionY, std::vector<std::vector<char>>& coordinates){
	int posX, posY;
	do{
		posX = distributionX(gen);
		posY = distributionY(gen);
	}while(coordinates[posY][posX] != ' ');
	food.posX = posX;
	food.posY = posY;
	coordinates[posY][posX] = food.base;
}

int main() {
	std::signal(SIGINT, signalHandler);
	std::signal(SIGQUIT, signalHandler);
	std::signal(SIGCONT, signalHandler);
	std::signal(SIGSEGV, signalHandler);

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
	
	head.posX = columns / 2;
	head.posY = lines / 2;
	std::uniform_int_distribution<int> distributionX(0, columns - 1);
	std::uniform_int_distribution<int> distributionY(0, lines - 1);
	
	coordinates[head.posY][head.posX] = head.base;
	generateFood(std::ref(distributionX), std::ref(distributionY), std::ref(coordinates));
	
	std::thread display(displayPosition, std::ref(coordinates));
	std::thread input(inputThread);

	while (!stopThread) {
		{
			std::unique_lock<std::mutex> lock1(coordinatesMutex);
			std::unique_lock<std::mutex> lock2(headMutex);
			
			switch (head.directionX){
				case 1:
					head.base = head.bases[3];
					break;
				case -1:
					head.base = head.bases[2];
					break;
			}
			switch (head.directionY){
				case 1:
					head.base = head.bases[1];
					break;
				case -1:
					head.base = head.bases[0];
					break;
			}
			coordinates[head.posY][head.posX] = head.base;
			
			if (head.directionY == 0){
				if ((head.posX == 0) && (head.directionX == -1)) {
					if (coordinates[head.posY][columns - 1] == tempBody.base){
						{std::unique_lock<std::mutex> lock0(stopThreadMutex);stopThread.store(true);}
						gameOver = true;
					}
					if (coordinates[head.posY][columns - 1] == food.base){
						coordinates[food.posY][food.posX] = ' ';
						foodCreation = true;
					}
					
					coordinates[head.posY][head.posX] ^= coordinates[head.posY][columns - 1];
					coordinates[head.posY][columns - 1] ^= coordinates[head.posY][head.posX];
					coordinates[head.posY][head.posX] ^= coordinates[head.posY][columns - 1];

					head.posX = columns - 1;
				} else if (((head.posX + 1) == columns) && (head.directionX == 1)) {
					if (coordinates[head.posY][0] == tempBody.base){
						{std::unique_lock<std::mutex> lock0(stopThreadMutex);stopThread.store(true);}
						gameOver = true;
					}
					if (coordinates[head.posY][0] == food.base){
						coordinates[food.posY][food.posX] = ' ';
						foodCreation = true;
					}
					
					coordinates[head.posY][head.posX] ^= coordinates[head.posY][0];
					coordinates[head.posY][0] ^= coordinates[head.posY][head.posX];
					coordinates[head.posY][head.posX] ^= coordinates[head.posY][0];

					head.posX = 0;
				} else{
					if (coordinates[head.posY][head.posX + head.directionX] == tempBody.base){
						{std::unique_lock<std::mutex> lock0(stopThreadMutex);stopThread.store(true);}
						gameOver = true;
					}
					if (coordinates[head.posY][head.posX + head.directionX] == food.base){
						coordinates[food.posY][food.posX] = ' ';
						foodCreation = true;
					}
					
					coordinates[head.posY][head.posX] ^= coordinates[head.posY][head.posX + head.directionX];
					coordinates[head.posY][head.posX + head.directionX] ^= coordinates[head.posY][head.posX];
					coordinates[head.posY][head.posX] ^= coordinates[head.posY][head.posX + head.directionX];

					head.posX += head.directionX;
				}
			} else if(head.directionX == 0){
				if ((head.posY == 0) && (head.directionY == -1)) {
					if (coordinates[lines - 1][head.posX] == tempBody.base){
						{std::unique_lock<std::mutex> lock0(stopThreadMutex);stopThread.store(true);}
						gameOver = true;
					}
					if (coordinates[lines - 1][head.posX] == food.base){
						coordinates[food.posY][food.posX] = ' ';
						foodCreation = true;
					}
					
					coordinates[head.posY][head.posX] ^= coordinates[lines - 1][head.posX];
					coordinates[lines - 1][head.posX] ^= coordinates[head.posY][head.posX];
					coordinates[head.posY][head.posX] ^= coordinates[lines - 1][head.posX];

					head.posY = lines - 1;
				} else if (((head.posY + 1) == lines) && (head.directionY == 1)) {
					if (coordinates[0][head.posX] == tempBody.base){
						{std::unique_lock<std::mutex> lock0(stopThreadMutex);stopThread.store(true);}
						gameOver = true;
					}
					if (coordinates[0][head.posX] == food.base){
						coordinates[food.posY][food.posX] = ' ';
						foodCreation = true;
					}
					
					coordinates[head.posY][head.posX] ^= coordinates[0][head.posX];
					coordinates[0][head.posX] ^= coordinates[head.posY][head.posX];
					coordinates[head.posY][head.posX] ^= coordinates[0][head.posX];

					head.posY = 0;
				} else{
					if (coordinates[head.posY + head.directionY][head.posX] == tempBody.base){
						{std::unique_lock<std::mutex> lock0(stopThreadMutex);stopThread.store(true);}
						gameOver = true;
					}
					if (coordinates[head.posY + head.directionY][head.posX] == food.base){
						coordinates[food.posY][food.posX] = ' ';
						foodCreation = true;
					}
					
					coordinates[head.posY][head.posX] ^= coordinates[head.posY + head.directionY][head.posX];
					coordinates[head.posY + head.directionY][head.posX] ^= coordinates[head.posY][head.posX];
					coordinates[head.posY][head.posX] ^= coordinates[head.posY + head.directionY][head.posX];

					head.posY += head.directionY;
				}
			}
			next(std::ref(coordinates));
			if (foodCreation){
				score++;
				generateBody(std::ref(coordinates));
				generateFood(std::ref(distributionX), std::ref(distributionY), std::ref(coordinates));
				foodCreation = false;
			}
		}
		std::this_thread::sleep_for(std::chrono::milliseconds(100));
	}

	display.join();
	input.join();
	endwin();
	if (gameOver){
		std::vector<std::string> gameoverMessages = {
			"Snake decided to play Twister with itself and lost. Game over!",
			"Oops! Snake thought it was a donut and took a bite out of itself. Game over.",
			"Snake tried to be fancy and perform a tail-knotting trick. It didn't end well. Game over!",
			"Looks like the snake was its own worst enemy. Game over!",
			"Snake got a little too hungry and mistook its tail for a snack. Game over.",
			"Snake's attempt at a self-hug didn't go as planned. Game over!"
		};
		std::uniform_int_distribution<int> dist(0, gameoverMessages.size() - 1);
		int randomIndex = dist(gen);
		std::cout << gameoverMessages[randomIndex] << std::endl;
	} else{std::cout << "Exited.." << std::endl;}
	return 0;
}