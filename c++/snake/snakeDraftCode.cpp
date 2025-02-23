//class Food;
//class Snake;

//std::unordered_set<std::pair<int, int>, boost::hash<std::pair<int, int>>> possiblePos;

//std::set<std::pair<std::reference_wrapper<int>, std::reference_wrapper<int>>> headsPos;
//std::set<std::pair<std::reference_wrapper<int>, std::reference_wrapper<int>>> partsPos;
//std::unordered_set<std::pair<int, int>, boost::hash<std::pair<int, int>>> partsPos;
//std::unordered_set<std::pair<int, int>, boost::hash<std::pair<int, int>>> foodsPos;

//std::unordered_map<std::pair<int, int>, Food, boost::hash<std::pair<int, int>>> foods;
//std::vector<Snake> snakes;

/*
struct PosX {
public:
	int value;
	
	friend struct PosX;
	friend class Head;
	friend class Part;
	friend class Snake;
	
	int pastValue;
	
	PosX(const int other = 0) : value(other % columns), pastValue(other % columns) {
		
	}
	
	PosX& operator=(const PosX& other) {
		pastValue = value;
		value = other.value;
		return *this;
	}
	
	PosX& operator=(int other) {
		pastValue = value;
		value = other % columns;
		return *this;
	}
	
	PosX& operator++() {
		pastValue = value;
		value = ++value % columns;
		return *this;
	}
	
	PosX& operator--() {
		pastValue = value;
		value = --value % columns;
		return *this;
	}
	
	PosX operator+(int other) const {
		return PosX(value + other);
	}
	
	PosX operator-(int other) const {
		return PosX(value - other);
	}
	
	int get() const {
		return value;
	}
	
	operator int() {
		return value;
	}
};

struct PosY {
public:
	int value;
	
	friend struct PosY;
	friend class Head;
	friend class Part;
	friend class Snake;
	
	int pastValue;
	
	PosY(const int other = 0) : positions(positions), value(other % lines), pastValue(other % lines) {}
	
	PosY& operator=(const PosY& other) {
		pastValue = value;
		value = other.value;
		return *this;
	}
	
	PosY& operator=(int other) {
		pastValue = value;
		value = other % lines;
		return *this;
	}
	
	PosY& operator++() {
		pastValue = value;
		value = ++value % lines;
		return *this;
	}
	
	PosY& operator--() {
		pastValue = value;
		value = --value % lines;
		return *this;
	}
	
	PosY operator+(int other) {
		return PosY(value + other);
	}
	
	PosY operator-(int other) {
		return PosY(value - other);
	}
	
	int get() const {
		return value;
	}
	
	operator int() {
		return value;
	}
};

struct Pos {
	PosX x;
	PosY y;
	
	std::unordered_set<std::pair<int, int>, boost::hash<std::pair<int, int>>>& positions;
	
	Pos(const std::unordered_set<std::pair<int, int>, boost::hash<std::pair<int, int>>>& positions, const int posX = 0, const int posY = 0) : positions(positions), x(posX), y(posY) {}
}

class Head {
public:
	char base = '^';
	const char bases[4] = {'^', 'v', '<', '>'};
	
	int directionX, directionY;
	PosX posX;
	PosY posY;
	Head(const int directionX = 0, const int directionY = -1, const int posX = 0, const int posY = 0) : directionX(directionX), directionY(directionY), posX(posX), posY(posY) {
		partsPos.emplace(posX.value, posY.value);
		updateBase();
	}
	
	void setDirectX(int value) {
		directionX = value;
		directionY = 0;
		updateBase();
	}
	
	void setDirectY(int value) {
		directionX = 0;
		directionY = value;
		updateBase();
	}

private:
	void updateBase() {
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
	
	PosX posX;
	PosY posY;
	
	Part(int posX, int posY) : posX(posX), posY(posY) {
		partsPos.emplace(posX.value, posY.value);
	}
};

class Food {
public:
	char base = '@';
	
	PosX posX;
	PosY posY;
	
	Food() = default;
	
	Food(const int posX, const int posY) : posX(posX), posY(posY) {}
	
	static Food& create(std::optional<int> posX = std::nullopt, std::optional<int> posY = std::nullopt) {
		std::unordered_set<std::pair<int, int>, boost::hash<std::pair<int, int>>> availsPos = possiblePos;
		
		for (const std::pair<int, int>& pos : partsPos) {
			availsPos.erase({pos.first, pos.second});
		} for (const std::pair<int, int>& pos : foodsPos) {
			availsPos.erase({pos.first, pos.second});
		}
		
		if (!(posX.has_value() || posY.has_value())) {
			std::vector<std::pair<int, int>> availsPosVec(availsPos.begin(), availsPos.end());
			std::uniform_int_distribution<> distr(0, availsPosVec.size() - 1);
			std::pair<int, int> availPos = availsPosVec[distr(gen)];
			
			posX = availPos.first;
			posY = availPos.second;
		} else if (posX.has_value() ^ posY.has_value()) {
			if (posX.has_value()) {
				posX = posX;
				
				for (auto it = std::begin(availsPos); it != std::end(availsPos);) {
					if (it->first != posX) {
						it = availsPos.erase(it);
					} else {
						++it;
					}
				}
				
			} else if (posY.has_value()) {
				posY = posY;
				
				for (auto it = std::begin(availsPos); it != std::end(availsPos);) {
					if (it->second != posY) {
						it = availsPos.erase(it);
					} else {
						++it;
					}
				}
			}
			
			std::vector<std::pair<int, int>> availsPosVec(availsPos.begin(), availsPos.end());
			std::uniform_int_distribution<> distr(0, availsPosVec.size() - 1);
			std::pair<int, int> availPos = availsPosVec[distr(gen)];
			
			posX = availPos.first;
			posY = availPos.second;
		} else {
			posX = posX;
			posY = posY;
		}
		
		foods[{posX.value(), posY.value()}] = Food(posX.value(), posY.value());
		return foods[{posX.value(), posY.value()}];
	}
	
	Food& ate(std::optional<int> posX = std::nullopt, std::optional<int> posY = std::nullopt) {
		foodsPos.erase({this->posX.get(), this->posY.get()});
		foods.erase({this->posX.get(), this->posY.get()});
		
		return Food::create(posX, posY);
	}
};

class Snake {
public:
	bool foodAte = false, gameOver = false;
	int score = 0;
	std::vector<Part> parts;
	Head head;
	
	Snake() = default;
	
	Snake(const int directionX, const int directionY, const int posX, const int posY) : head(directionX, directionY, posX, posY) {}
	
	static Snake& create(const int directionX = 0, const int directionY = -1, const int posX = columns / 2, const int posY = lines / 2) {
		snakes.emplace_back(directionX, directionY, posX, posY);
		return snakes.back();
	}
	
	void nextH() {
		if (head.directionY == 0) {
			if (head.posX == 0 && head.directionX == -1) {
				
			} else if (head.posX == columns - 1 && head.directionX == 1) {
				
			} else {
				
			}
		} else if (head.directionX == 0) {
			if (head.posY == 0 && head.directionY == -1) {
				
			} else if (head.posY == lines - 1 && head.directionY == 1) {
				
			} else {
				
			}
		}
	}
};

struct PairHash {
	std::size_t operator()(const std::pair<std::reference_wrapper<int>, std::reference_wrapper<int>>& p) const {
		std::size_t seed = 0;
		// Use boost::hash_combine for efficient hashing
		boost::hash_combine(seed, p.first.get());
		boost::hash_combine(seed, p.second.get());
		return seed;
	}
};

int main() {
	int a = 10, b = 20, c = 30, d = 40;
	std::unordered_set<std::pair<std::reference_wrapper<int>, std::reference_wrapper<int>>, PairHash> tests;
	
	tests.emplace(std::make_pair(std::ref(a), std::ref(b)));
	tests.emplace(std::make_pair(std::ref(c), std::ref(d)));
	
	for (const auto& pair : tests) {
		std::cout << pair.first << ", " << pair.second << std::endl;
	}
	
	a *= 10;
	b *= 10;
	
	for (const auto& pair : tests) {
		std::cout << pair.first << ", " << pair.second << std::endl;
	}
}
*/