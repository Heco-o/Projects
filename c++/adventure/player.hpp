#ifndef PLAYER_HPP
#define PLAYER_HPP

#include <vector>
#include <string>
#include <limits>
#include <optional>

struct Attribute {
	double value;
	std::optional<double> min;
	std::optional<double> max;
	
	Attribute(double value, std::optional<double> max = std::nullopt, std::optional<double> min = 0) : value(value), min(min), max(max) {
		if (max.has_value() && min.has_value()) {
			if (min.value() > max.value()) {
				this->max = min.value();
			} if (value > max.value()) {
				this->value = max.value();
			} else if (value < min.value()) {
				this->value = min.value();
			}
		} else if (max.has_value() && value > max.value()) {
			this->value = max.value();
		} else if (min.has_value() && value < min.value()) {
			this->value = min.value();
		}
	}
	
	template<typename T>
	Attribute& operator+(T value) {
		value = static_cast<double>(value);
		if (max.has_value()) {
			if (this->value + value > max.value()) {
				this->value = max.value();
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
		if (min.has_value()) {
			if (this->value - value < min.value()) {
				this->value = min.value();
			} else {
				this->value -= value;
			}
		} else {
			this->value -= value;
		}
		return *this;
	}
	
	template<typename T>
	Attribute& operator=(T value) {
		value = static_cast<double>(value);
		if (max.has_value() && min.has_value()) {
			if (value > max.value()) {
				this->value = max.value();
			} else if (value < min.value()) {
				this->value = min.value();
			} else {
				this->value = value;
			}
		} else if (max.has_value()) {
			if (value > max.value()) {
				this->value = max.value();
			} else {
				this->value = value;
			}
		} else if (min.has_value()) {
			if (value < min.value()) {
				this->value = min.value();
			} else {
				this->value = value;
			}
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
		if (inv.size() < capacity) {
			inv.push_back(item);
		}
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