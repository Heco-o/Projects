#include <iostream>
#include <boost/functional/hash.hpp>
#include <random>
#include <utility>
#include <vector>
#include <deque>
#include <unordered_set>
#include <unordered_map>
#include <memory>
#include <ncurses.h>
#include <thread>
#include <chrono>
#include <atomic>
#include <mutex>

#ifdef _WIN32
	#include <windows.h>
#else
	#include <sys/ioctl.h>
	#include <unistd.h>
#endif

constexpr uint64_t FREQ = 19200000;

std::random_device rd;
std::mt19937 gen(rd());

std::unordered_set<std::pair<int, int>, boost::hash<std::pair<int, int>>> possiblePos;

std::atomic<bool> gameNotOver(true);
std::atomic<uint64_t> ticks(0), frames(0), totalTicks(0), totalFrames(0), columns(0), lines(0), section(0);
std::atomic<double> avgFPS(0), avgTPS(0);
std::mutex snakeMutex;

class Head;
class Part;
class Food;
class Snake;

std::unordered_set<std::pair<int, int>, boost::hash<std::pair<int, int>>> partsPos;
std::unordered_set<std::pair<int, int>, boost::hash<std::pair<int, int>>> foodsPos;

std::unordered_map<std::pair<int, int>, Food, boost::hash<std::pair<int, int>>> foods;
std::vector<Snake> snakes;

inline int pyMod(const int dividend, const int divisor) noexcept {
	const int result = dividend % divisor;
	return result < 0 ? result + divisor : result;
}

class Head {
public:
	char base = '^';
	const char bases[4] = {'^', 'v', '<', '>'};
	
	int directionX, directionY, posX, posY, prevPosX, prevPosY;
	
	Head(const int directionX = 0, const int directionY = -1, const int iPosX = 0, const int iPosY = 0) : directionX(directionX), directionY(directionY), posX(pyMod(iPosX, columns)), posY(pyMod(iPosY, lines)) {
		possiblePos.erase({posX, posY});
		partsPos.emplace(posX, posY);
		prevPosX = posX;
		prevPosY = posY;
		updateBase();
	}
	
	inline void setDirectX(const int value) noexcept {
		if (directionY == 0) {
			return;
		}
		directionX = value;
		directionY = 0;
		updateBase();
	}
	
	inline void setDirectY(const int value) noexcept {
		if (directionX == 0) {
			return;
		}
		directionX = 0;
		directionY = value;
		updateBase();
	}
	
	inline void setPos(const int iPosX, const int iPosY) {
		possiblePos.emplace(posX, posY);
		partsPos.erase({posX, posY});
		prevPosX = posX;
		prevPosY = posY;
		posX = pyMod(iPosX, columns);
		posY = pyMod(iPosY, lines);
		possiblePos.erase({posX, posY});
		partsPos.emplace(posX, posY);
	}
	
private:
	void updateBase() noexcept {
		switch (directionX) {
			case 1:
				base = bases[3];
				break;
			case -1:
				base = bases[2];
				break;
		}
		switch (directionY) {
			case 1:
				base = bases[1];
				break;
			case -1:
				base = bases[0];
				break;
		}
	}
};

class Part {
public:
	char base = '#';
	
	int posX, posY;
	
	Part(const int iPosX, const int iPosY) : posX(pyMod(iPosX, columns)), posY(pyMod(iPosY, lines)) {
		possiblePos.erase({posX, posY});
		partsPos.emplace(posX, posY);
	}
	
	inline void setPos(const int iPosX, const int iPosY) {
		possiblePos.emplace(posX, posY);
		partsPos.erase({posX, posY});
		posX = pyMod(iPosX, columns);
		posY = pyMod(iPosY, lines);
		possiblePos.erase({posX, posY});
		partsPos.emplace(posX, posY);
	}
};

class Food {
public:
	char base = '@';
	
	int posX, posY;
	
	Food() = default;
	
	Food(const int iPosX, const int iPosY) : posX(pyMod(iPosX, columns)), posY(pyMod(iPosY, lines)) {
		possiblePos.erase({posX, posY});
		foodsPos.emplace(posX, posY);
	}
	
	static Food* create(const std::optional<int> oPosX = std::nullopt, const std::optional<int> oPosY = std::nullopt) {
		if (possiblePos.empty()) {
			return nullptr;
		} else if (oPosX.has_value() && oPosY.has_value()) {
			if (possiblePos.find({oPosX.value(), oPosY.value()}) == possiblePos.end()) {
				return nullptr;
			}
			
			return &foods.emplace(std::make_pair(oPosX.value(), oPosY.value()), Food(oPosX.value(), oPosY.value())).first->second;
		} else if (oPosX.has_value()) {
			std::vector<std::pair<int, int>> selectedPos;
			selectedPos.reserve(possiblePos.size());
			const int iPosX = oPosX.value();
			
			std::copy_if(possiblePos.begin(), possiblePos.end(), std::back_inserter(selectedPos), [iPosX](const std::pair<int, int>& pair) {
				return pair.first == iPosX;
			});
			
			if (selectedPos.empty()) {
				return nullptr;
			}
			
			std::uniform_int_distribution<> distr(0, selectedPos.size() - 1);
			
			const std::pair<int, int> randomPos = selectedPos[distr(gen)];
			
			return &foods.emplace(randomPos, Food(randomPos.first, randomPos.second)).first->second;
		} else if (oPosY.has_value()) {
			std::vector<std::pair<int, int>> selectedPos;
			selectedPos.reserve(possiblePos.size());
			const int iPosY = oPosY.value();
			
			std::copy_if(possiblePos.begin(), possiblePos.end(), std::back_inserter(selectedPos), [iPosY](const std::pair<int, int>& pair) {
				return pair.second == iPosY;
			});
			
			if (selectedPos.empty()) {
				return nullptr;
			}
			
			std::uniform_int_distribution<> distr(0, selectedPos.size() - 1);
			const std::pair<int, int> randomPos = selectedPos[distr(gen)];
			
			return &foods.emplace(randomPos, Food(randomPos.first, randomPos.second)).first->second;
		} else {
			std::uniform_int_distribution<> distr(0, possiblePos.size() - 1);
			const std::pair<int, int> randomPos = *std::next(possiblePos.begin(), distr(gen));
			
			return &foods.emplace(randomPos, Food(randomPos.first, randomPos.second)).first->second;
		}
	}
	
	Food* ate(std::optional<int> oPosX = std::nullopt, std::optional<int> oPosY = std::nullopt) const {
		foodsPos.erase({posX, posY});
		foods.erase({posX, posY});
		
		return create(oPosX, oPosY);
	}
};

class Snake {
public:
	bool foodAte = false, gameOver = false;
	int score = 0;
	std::pair<int, int> lastPos{0, 0};
	std::deque<Part> parts;
	Head head;
	
	Snake() = default;
	
	Snake(const int directionX, const int directionY, const int posX, const int posY) : head(directionX, directionY, posX, posY) {}
	
	static Snake& create(const int directionX = 0, const int directionY = -1, const int posX = columns / 2, const int posY = lines / 2) {
		snakes.emplace_back(directionX, directionY, posX, posY);
		return snakes.back();
	}
	
	void nextH() {
		const int nextPosX = pyMod((head.posX + head.directionX), columns);
		const int nextPosY = pyMod((head.posY + head.directionY), lines);
		
		if (partsPos.find({nextPosX, nextPosY}) != partsPos.end()) {
			gameOver = true;
		}
		
		if (foodsPos.find({nextPosX, nextPosY}) != partsPos.end()) {
			foodAte = true;
		}
		
		head.setPos(nextPosX, nextPosY);
	}
	
	void nextP() {
		if (!parts.empty()) {
			Part& part = parts.back();
			lastPos = {part.posX, part.posY};
			part.setPos(head.prevPosX, head.prevPosY);
			parts.push_front(std::move(part));
			parts.pop_back();
		}
	}
	
	void generatePart() {
		if (parts.empty()) {
			parts.emplace_back(head.prevPosX, head.prevPosY);
		} else {
			parts.emplace_back(lastPos.first, lastPos.second);
		}
	}
	
	void update() {
		nextH();
		nextP();
		if (foodAte) {
			++score;
			generatePart();
			foods[{head.posX, head.posY}].ate();
			foodAte = false;
		}
	}
};

void renderScreen() {
	//auto startTime = std::chrono::high_resolution_clock::now();
	uint64_t startTime, currentTime, totalStartTime, totalEndTime;
	double fps = 0, tps = 0, passedTime = 0;
	asm volatile("mrs %0, cntvct_el0" : "=r"(startTime));
	clear();
	asm volatile("mrs %0, cntvct_el0" : "=r"(totalStartTime));
	while (gameNotOver) {
		erase();
		{
			std::lock_guard<std::mutex> lock1(snakeMutex);
			
			for (int i = 0; i < snakes.size(); ++i) {
				if (i == section) {
					attron(COLOR_PAIR(1));
					mvaddch(snakes[i].head.posY, snakes[i].head.posX, snakes[i].head.base);
					for (const Part& part : snakes[i].parts) {
						mvaddch(part.posY, part.posX, part.base);
					} attroff(COLOR_PAIR(1));
				} else {
					mvaddch(snakes[i].head.posY, snakes[i].head.posX, snakes[i].head.base);
					for (const Part& part : snakes[i].parts) {
						mvaddch(part.posY, part.posX, part.base);
					}
				}
			}
			
			for (const std::pair<std::pair<int, int>, Food>& pair : foods) {
				mvaddch(pair.second.posY, pair.second.posX, pair.second.base);
			}
			move(lines, 0);
			/*
			if (std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - startTime).count() >= 1) {
				tps = ticks;
				fps = frames;
				ticks = 0;
				frames = 0;
				startTime = std::chrono::high_resolution_clock::now();
			}
			*/
			asm volatile("mrs %0, cntvct_el0" : "=r"(currentTime));
			passedTime = (currentTime - startTime);
			if (passedTime >= FREQ) {
				tps = ticks * FREQ/passedTime;
				fps = frames * FREQ/passedTime;
				ticks = frames = currentTime = 0;
				asm volatile("mrs %0, cntvct_el0" : "=r"(startTime));
			}
			
			printw("FPS: %f, ", fps);
			printw("TPS: %f, ", tps);
			
			int i = 0;
			for (const Snake& snake : snakes) {
				if (i == section) {
					attron(COLOR_PAIR(1));
					printw("Score%d: %d, ", i, snake.score);
					attroff(COLOR_PAIR(1));
				} else {
					printw("Score%d: %d, ", i, snake.score);
				}
				++i;
			}
			
		}
		refresh();
		++frames;
		++totalFrames;
		std::this_thread::sleep_for(std::chrono::milliseconds(10));
	}
	asm volatile("mrs %0, cntvct_el0" : "=r"(totalEndTime));
	passedTime = (totalEndTime - totalStartTime);
	avgFPS = totalFrames * FREQ / passedTime;
	avgTPS = totalTicks * FREQ / passedTime;
}

void userInput() {
	while (gameNotOver) {
		switch (getch()) {
			case KEY_UP:
				snakes[section].head.setDirectY(-1);
				break;
			case KEY_DOWN:
				snakes[section].head.setDirectY(1);
				break;
			case KEY_LEFT:
				snakes[section].head.setDirectX(-1);
				break;
			case KEY_RIGHT:
				snakes[section].head.setDirectX(1);
				break;
			case 27:
				gameNotOver.store(false);
				break;
			case '\t':
				if (section >= snakes.size() - 1) {
					section = 0;
				} else{
					++section;
				}
				break;
		}
	}
}

// GPT generated.
void getTerminalSize() {
#ifdef _WIN32
	CONSOLE_SCREEN_BUFFER_INFO csbi;
	if (GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &csbi)) {
		columns = csbi.srWindow.Right - csbi.srWindow.Left + 1;
		lines = csbi.srWindow.Bottom - csbi.srWindow.Top;
	} else {
		std::cerr << "Unable to get terminal size on Windows." << std::endl;
		columns = lines = -1;
	}
#else
	struct winsize w;
	if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &w) == 0) {
		columns = w.ws_col;
		lines = w.ws_row - 1;
	} else {
		std::cerr << "Unable to get terminal size on POSIX system." << std::endl;
		columns = lines = -1;
	}
#endif
}

int main(int argc, char* argv[]) {
	getTerminalSize();
	for (int i = 0; i < columns; ++i) {
		for (int j = 0; j < lines; ++j) {
			possiblePos.emplace(i, j);
		}
	}
	
	const int snakesNum = argc > 1 ? std::stoi(argv[1]) : 1;
	const int foodsNum = argc > 2 ? std::stoi(argv[2]) : 1;
	
	for (int i = 0; i < snakesNum; ++i) {
		Snake::create(0, -1, (i + 1) * columns / (snakesNum + 1));
	} for (int i = 0; i < foodsNum; ++i) {
		Food::create();
	}
	
	initscr();
	cbreak();
	noecho();
	start_color();
	keypad(stdscr, TRUE);
	curs_set(0);
	init_pair(1, COLOR_BLUE, COLOR_BLACK);
	
	std::thread render(renderScreen);
	std::thread input(userInput);
	
	while (gameNotOver) {
		{
			std::lock_guard<std::mutex> lock1(snakeMutex);
			
			for (Snake& snake : snakes) {
				snake.update();
				if (snake.gameOver) {
					gameNotOver.store(false);
				}
			}
		}
		++ticks;
		++totalTicks;
		std::this_thread::sleep_for(std::chrono::milliseconds(100));
	}
	
	render.join();
	input.join();
	
	endwin();
	
	std::cout << "Average Frames: " << avgFPS << std::endl;
	std::cout << "Average Ticks: " << avgTPS << std::endl;
}