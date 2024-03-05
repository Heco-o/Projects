#ifndef PLAYER_HPP
#define PLAYER_HPP

#include <vector>

struct Attribute {
	double value;
	double max = 0;
	
	Attribute(double value) : value(value) {}
	Attribute(double value, double max) : value(value) {
		if (value > max && max > 0) {
			this->value = max;
		}
	}
	
	template<typename T>
	Attribute& operator+(T value) {
		value = static_cast<double>(value);
		if (max > 0) {
			if (this->value + value > max) {
				this->value = max;
			} else {
				this->value += value;
			}
		} else {
			this->value += value;
		}
		return *this;
	}
	
	template<typename T>
	Attribute& operator-(T value) {
		value = static_cast<double>(value);
		if (this->value - value < 0) {
			this->value = 0;
		} else {
			this->value -= value;
		}
		return *this;
	}
	
	template<typename T>
	Attribute& operator=(T value) {
		value = static_cast<double>(value);
		if (value > max && max > 0) {
			this->value = max;
		} else if (value < 0) {
			this->value = 0;
		} else {
			this->value = value;
		}
		return *this;
	}
	
	operator double() {
		return value;
	}
};
struct Inventory {
	int capacity;
	std::vector<Item> inv;
	
	Inventory(int capacity) : capacity(capacity) {}
	
	void add(Item item) {
		inv.push_back(item);
	}
};

class Player {
public:
	std::string name = "Player";
	
	Attribute health{100, 100};
	Attribute money{0};
	Attribute resistance{0};
	Attribute stamina{100, 100};
	Attribute power{0};
	Attribute fatigue{0, 100};
	Attribute dodgeChance{2, 100};
	Attribute defence{0};
	Attribute strength{0};
};

#endif