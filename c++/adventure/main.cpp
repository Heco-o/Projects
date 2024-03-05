#include "item.hpp"
#include "player.hpp"
#include <iostream>

int main() {
	Player player;
	
	player.health + 20;
	std::cout << "Health: " << player.health << std::endl;
	player.health - 200;
	std::cout << "Health: " << player.health << std::endl;
	
	player.stamina - 30;
	std::cout << "Stamina: " << player.stamina << std::endl;
	player.stamina + 200;
	std::cout << "Stamina: " << player.stamina << std::endl;

	return 0;
}