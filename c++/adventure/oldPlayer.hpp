#ifndef PLAYER_HPP
#define PLAYER_HPP

#include <string>

struct Attribute {
	double value;
	double max = 0;

	Attribute(double value);
	Attribute(double value, double max);
	template<typename T>
	Attribute& operator+(T value);
	template<typename T>
	Attribute& operator-(T value);
	operator double();
};

class Player {
public:
	std::string name = "Player";

	Attribute health{100, 100};
	Attribute money{0};
	Attribute resistance{0};
	Attribute stamina{100, 100};
	Attribute power{0};
	Attribute fatigue{0};
	Attribute dodgeChance{2, 100};
};

#endif