#include <string>

/*
struct Item {
	std::string name;
	int quantity;
	double grade;
	double durability;
	double damage;
	double baseDurability;
	double baseDamage;

	Item(int quantity, std::string name, double grade, double durability, double damage) {
		this->quantity = quantity;
		this->name = name;
		this->grade = grade;
		this->durability = durability * grade;
		this->damage = damage * grade;
		baseDurability = durability;
		baseDamage = damage;
	}
};*/

class Item {
	public:
	std::string name = "";
	std::string description = "";
};