#include <iostream>
#include <unistd.h>
#include <ncurses.h>
#include <sys/ioctl.h>
#include <vector>
#include <random>
#include <thread>
#include <chrono>
#include <atomic>
#include <mutex>

std::random_device rd;
std::mt19937 gen(rd());

int lines, columns, frames, section = 0;
double fps;
bool gameOver = false;
std::atomic<bool> stopThread(false);

std::mutex stopThreadMutex;
std::mutex coordinatesMutex;
std::mutex snakeMutex;

struct Part {
	char base, bases[4];
	int directionX, directionY, pastX, pastY, posX, posY;
};

struct Food{
	char base = '@';
	int posX, posY;
};

class Snake {
	std::vector<std::vector<char>>& coordinates;
	std::uniform_int_distribution<int> distributionX;
	std::uniform_int_distribution<int> distributionY;
public:
	int lines, columns, score;
	bool foodCreation, gameOver = false;
	char bodyBase = '#';
	Food food;
	std::vector<Part> parts;
	
	Snake(std::vector<std::vector<char>>& vec, const Part head) : coordinates(vec), distributionX(0, vec[0].size() - 1), distributionY(0, vec.size() - 1) {
		lines = vec.size();
		columns = vec[0].size();
		parts.push_back(head);
	}
	
	void next() {
		switch (parts[0].directionX){
			case 1:
				parts[0].base = parts[0].bases[3];
				break;
			case -1:
				parts[0].base = parts[0].bases[2];
				break;
		}
		switch (parts[0].directionY){
			case 1:
				parts[0].base = parts[0].bases[1];
				break;
			case -1:
				parts[0].base = parts[0].bases[0];
				break;
		}
		coordinates[parts[0].posY][parts[0].posX] = parts[0].base;
		
		if (parts[0].directionY == 0){
			if ((parts[0].posX == 0) && (parts[0].directionX == -1)) {
				if (coordinates[parts[0].posY][columns - 1] == bodyBase){
					gameOver = true;
				} else {
					for (int i = 0; i < 4; i++) {
						if (coordinates[parts[0].posY][columns - 1] == parts[0].bases[i]){
							gameOver = true;
						}
					}
				}
				
				if (coordinates[parts[0].posY][columns - 1] == food.base){
					coordinates[food.posY][food.posX] = ' ';
					foodCreation = true;
				}
				
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[parts[0].posY][columns - 1];
				coordinates[parts[0].posY][columns - 1] ^= coordinates[parts[0].posY][parts[0].posX];
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[parts[0].posY][columns - 1];
				
				parts[0].posX = columns - 1;
			} else if (((parts[0].posX + 1) == columns) && (parts[0].directionX == 1)) {
				if (coordinates[parts[0].posY][0] == bodyBase){
					gameOver = true;
				} else {
					for (int i = 0; i < 4; i++) {
						if (coordinates[parts[0].posY][0] == parts[0].bases[i]){
							gameOver = true;
						}
					}
				}
				
				if (coordinates[parts[0].posY][0] == food.base){
					coordinates[food.posY][food.posX] = ' ';
					foodCreation = true;
				}
				
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[parts[0].posY][0];
				coordinates[parts[0].posY][0] ^= coordinates[parts[0].posY][parts[0].posX];
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[parts[0].posY][0];
				
				parts[0].posX = 0;
			} else{
				if (coordinates[parts[0].posY][parts[0].posX + parts[0].directionX] == bodyBase){
					gameOver = true;
				} else {
					for (int i = 0; i < 4; i++) {
						if (coordinates[parts[0].posY][parts[0].posX + parts[0].directionX] == parts[0].bases[i]){
							gameOver = true;
						}
					}
				}
				
				if (coordinates[parts[0].posY][parts[0].posX + parts[0].directionX] == food.base){
					coordinates[food.posY][food.posX] = ' ';
					foodCreation = true;
				}
				
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[parts[0].posY][parts[0].posX + parts[0].directionX];
				coordinates[parts[0].posY][parts[0].posX + parts[0].directionX] ^= coordinates[parts[0].posY][parts[0].posX];
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[parts[0].posY][parts[0].posX + parts[0].directionX];
				
				parts[0].posX += parts[0].directionX;
			}
		} else if(parts[0].directionX == 0){
			if ((parts[0].posY == 0) && (parts[0].directionY == -1)) {
				if (coordinates[lines - 1][parts[0].posX] == bodyBase){
					gameOver = true;
				} else {
					for (int i = 0; i < 4; i++) {
						if (coordinates[lines - 1][parts[0].posX] == parts[0].bases[i]){
							gameOver = true;
						}
					}
				}
				
				if (coordinates[lines - 1][parts[0].posX] == food.base){
					coordinates[food.posY][food.posX] = ' ';
					foodCreation = true;
				}
				
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[lines - 1][parts[0].posX];
				coordinates[lines - 1][parts[0].posX] ^= coordinates[parts[0].posY][parts[0].posX];
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[lines - 1][parts[0].posX];
				
				parts[0].posY = lines - 1;
			} else if (((parts[0].posY + 1) == lines) && (parts[0].directionY == 1)) {
				if (coordinates[0][parts[0].posX] == bodyBase){
					gameOver = true;
				} else {
					for (int i = 0; i < 4; i++) {
						if (coordinates[0][parts[0].posX] == parts[0].bases[i]){
							gameOver = true;
						}
					}
				}
				
				if (coordinates[0][parts[0].posX] == food.base){
					coordinates[food.posY][food.posX] = ' ';
					foodCreation = true;
				}
				
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[0][parts[0].posX];
				coordinates[0][parts[0].posX] ^= coordinates[parts[0].posY][parts[0].posX];
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[0][parts[0].posX];
				
				parts[0].posY = 0;
			} else{
				if (coordinates[parts[0].posY + parts[0].directionY][parts[0].posX] == bodyBase){
					gameOver = true;
				} else {
					for (int i = 0; i < 4; i++) {
						if (coordinates[parts[0].posY + parts[0].directionY][parts[0].posX] == parts[0].bases[i]){
							gameOver = true;
						}
					}
				}
				
				if (coordinates[parts[0].posY + parts[0].directionY][parts[0].posX] == food.base){
					coordinates[food.posY][food.posX] = ' ';
					foodCreation = true;
				}
				
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[parts[0].posY + parts[0].directionY][parts[0].posX];
				coordinates[parts[0].posY + parts[0].directionY][parts[0].posX] ^= coordinates[parts[0].posY][parts[0].posX];
				coordinates[parts[0].posY][parts[0].posX] ^= coordinates[parts[0].posY + parts[0].directionY][parts[0].posX];
	
				parts[0].posY += parts[0].directionY;
			}
		}
	}
	
	void next2() {
		for (int i = 1; i < parts.size(); i++){
			if (parts[i - 1].pastY == 0){
				if ((parts[i].posX == 0) && (parts[i - 1].pastX == -1)) {
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[parts[i].posY][columns - 1];
					coordinates[parts[i].posY][columns - 1] ^= coordinates[parts[i].posY][parts[i].posX];
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[parts[i].posY][columns - 1];
					
					parts[i].posX = columns - 1;
				} else if (((parts[i].posX + 1) == columns) && (parts[i - 1].pastX == 1)) {
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[parts[i].posY][0];
					coordinates[parts[i].posY][0] ^= coordinates[parts[i].posY][parts[i].posX];
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[parts[i].posY][0];
					
					parts[i].posX = 0;
				} else{
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[parts[i].posY][parts[i].posX + parts[i - 1].pastX];
					coordinates[parts[i].posY][parts[i].posX + parts[i - 1].pastX] ^= coordinates[parts[i].posY][parts[i].posX];
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[parts[i].posY][parts[i].posX + parts[i - 1].pastX];
					
					parts[i].posX += parts[i - 1].pastX;
				}
			} else if (parts[i - 1].pastX == 0){
				if ((parts[i].posY == 0) && (parts[i - 1].pastY == -1)) {
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[lines - 1][parts[i].posX];
					coordinates[lines - 1][parts[i].posX] ^= coordinates[parts[i].posY][parts[i].posX];
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[lines - 1][parts[i].posX];
					
					parts[i].posY = lines - 1;
				} else if (((parts[i].posY + 1) == lines) && (parts[i - 1].pastY == 1)) {
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[0][parts[i].posX];
					coordinates[0][parts[i].posX] ^= coordinates[parts[i].posY][parts[i].posX];
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[0][parts[i].posX];
					
					parts[i].posY = 0;
				} else{
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[parts[i].posY + parts[i - 1].pastY][parts[i].posX];
					coordinates[parts[i].posY + parts[i - 1].pastY][parts[i].posX] ^= coordinates[parts[i].posY][parts[i].posX];
					coordinates[parts[i].posY][parts[i].posX] ^= coordinates[parts[i].posY + parts[i - 1].pastY][parts[i].posX];
					
					parts[i].posY += parts[i - 1].pastY;
				}
			}
			parts[i].pastX = parts[i].directionX;
			parts[i].pastY = parts[i].directionY;
			parts[i].directionX = parts[i - 1].pastX;
			parts[i].directionY = parts[i - 1].pastY;
		}
		parts[0].pastX = parts[0].directionX;
		parts[0].pastY = parts[0].directionY;
	}
	
	void generateBody() {
		int currentSize = parts.size() - 1;
		Part body;
		body.base = bodyBase;
		body.directionX = parts[currentSize].pastX;
		body.directionY = parts[currentSize].pastY;
		body.posX = parts[currentSize].posX - parts[currentSize].directionX;
		body.posY = parts[currentSize].posY - parts[currentSize].directionY;
		coordinates[body.posY][body.posX] = body.base;
		
		parts.push_back(body);
	}
	
	void generateFood() {
		int posX, posY;
		do{
			posX = distributionX(gen);
			posY = distributionY(gen);
		}while(coordinates[posY][posX] != ' ');
		food.posX = posX;
		food.posY = posY;
		coordinates[posY][posX] = food.base;
	}
	
	void createFoodIf() {
		if (foodCreation) {
			score++;
			generateBody();
			generateFood();
			foodCreation = false;
		}
	}
};

bool getTerminalSize() {
	struct winsize ws;
	if (ioctl(STDOUT_FILENO, TIOCGWINSZ, & ws) != -1) {
		columns = ws.ws_col - 1;
		lines = ws.ws_row - 1;
		return true;
	} else {
		std::cerr << "Error retrieving terminal information." << std::endl;
		return false;
	}
}

void displayPosition(const std::vector<std::vector<char>>& coordinates, std::vector<Snake>& snakes) {
	std::chrono::steady_clock::time_point lastFrameTime = std::chrono::steady_clock::now();
	while (!stopThread) {
		{
			std::unique_lock <std::mutex> lock1(coordinatesMutex);
			clear();
			for (int i = 0; i < lines; i++) {
				for (int j = 0; j < columns; j++) {
					printw("%c", coordinates[i][j]);
				}
				printw("\n");
			}
		}
		
		{
			std::unique_lock<std::mutex> lock2(snakeMutex);
			init_pair(1, COLOR_BLUE, COLOR_BLACK);
			attron(COLOR_PAIR(1));
			for (auto& part : snakes[section].parts) {
				mvprintw(part.posY, part.posX, "%c", part.base);
			}
			attroff(COLOR_PAIR(1));
			mvprintw(lines, 0, "%c", ' ');
			
			for (int i = 0; i < snakes.size(); i++) {
				if (i == section) {
					attron(COLOR_PAIR(1));
					printw("Score%d: %d, ", i, snakes[i].score);
					attroff(COLOR_PAIR(1));
				} else {
					printw("Score%d: %d, ", i, snakes[i].score);
				}
			}
		}
		
		frames++;
		std::chrono::steady_clock::time_point currentTime = std::chrono::steady_clock::now();
		std::chrono::duration < double > elapsedSeconds = currentTime - lastFrameTime;
		if (elapsedSeconds.count() >= 1.0) {
			fps = frames / elapsedSeconds.count();
			lastFrameTime = currentTime;
			frames = 0;
		}
		printw("FPS: %.2f", fps);
		refresh();
		std::this_thread::sleep_for(std::chrono::milliseconds(10));
	}
}

void inputThread(std::vector<Snake>& snakes) {
	int ch;
	while (!stopThread) {
		ch = getch();
		{
			std::unique_lock<std::mutex> lock2(snakeMutex);
			
			switch (ch) {
				case 27:
					{
						std::unique_lock<std::mutex> lock0(stopThreadMutex);
						stopThread.store(true);
					}
					break;
				case KEY_LEFT:
					if (snakes[section].parts[0].directionX != 1){
						snakes[section].parts[0].directionX = -1;
						snakes[section].parts[0].directionY = 0;
					}
					break;
				case KEY_UP:
					if (snakes[section].parts[0].directionY != 1){
						snakes[section].parts[0].directionX = 0;
						snakes[section].parts[0].directionY = -1;
					}
					break;
				case KEY_RIGHT:
					if (snakes[section].parts[0].directionX != -1){
						snakes[section].parts[0].directionX = 1;
						snakes[section].parts[0].directionY = 0;
					}
					break;
				case KEY_DOWN:
					if (snakes[section].parts[0].directionY != -1){
						snakes[section].parts[0].directionX = 0;
						snakes[section].parts[0].directionY = 1;
					}
					break;
				case '\t':
					if (section == snakes.size() - 1) {
						section = 0;
					} else {
						section++;
					}
					break;
			}
		}
	}
}

void makeHeads(std::vector<Part>& heads, const int numHeads) {
	for (int i = 0; i < numHeads; i++) {
		Part head = {
			.bases = {'^', 'v', '<', '>'},
			.directionX = 0,
			.directionY = -1,
			.posX = (i + 1) * columns / (numHeads + 1),
			.posY = lines / 2
		};
		
		heads.push_back(head);
	}
}

int main(int argc, char* argv[]) {
	if (argc != 2) {
		std::cerr << "Usage: " << argv[0] << " <num_snakes>" << std::endl;
		return 1;
	}
	int snakesNum = std::stoi(argv[1]);
	
	if (!getTerminalSize()) { return 1; }
	std::vector<std::vector<char>> coordinates(lines, std::vector<char>(columns, ' '));
	std::vector<Snake> snakes;
	std::vector<Part> heads;
	
	makeHeads(std::ref(heads), snakesNum);
	
	if (heads.size() <= 0) {
		return 1;
	}
	
	for (Part head : heads) {
		snakes.push_back(Snake(std::ref(coordinates), head));
	}
	
	initscr();
	cbreak();
	start_color();
	keypad(stdscr, TRUE);
	
	std::thread display(displayPosition, std::ref(coordinates), std::ref(snakes));
	std::thread input(inputThread, std::ref(snakes));
	
	snakes[0].generateFood();
	while (!stopThread) {
		{
			std::unique_lock <std::mutex> lock1(coordinatesMutex);
			std::unique_lock<std::mutex> lock2(snakeMutex);
			
			for (Snake& snake : snakes) {
				snake.next();
				snake.next2();
				snake.createFoodIf();
				
				if (snake.gameOver) {
					{std::unique_lock<std::mutex> lock0(stopThreadMutex);stopThread.store(true);}
					gameOver = true;
					break;
				}
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
		std::cout << gameoverMessages[dist(gen)] << std::endl;
		for (int i = 0; i < snakes.size(); i++) {
			std::cout << "score" << i << ": " << snakes[i].score << std::endl;
		}
	} else{std::cout << "Exited.." << std::endl;}
	return 0;
}