#include <iostream>
#include <random>
#include <algorithm>
#include <vector>
#include <tuple>
#include <set>

std::random_device rd;
std::mt19937 gen(rd());

int main() {
	std::unordered_map<std::string, double> dict;
	dict["player1"] = 0;
	dict["player2"] = 0;
	dict["draw"] = 0;
	int games = 0;
	std::set<std::vector<std::tuple<std::string, std::string>>> positions;
	while (true) {
		const std::vector<std::string> cards = {"king", "servant", "slave"};
		std::vector<std::string> player1 = {"king", "king", "servant", "servant", "slave", "slave"};
		std::vector<std::string> player2 = {"king", "king", "servant", "servant", "slave", "slave"};
		int point1 = 0;
		int point2 = 0;
		bool state1 = false;
		bool state2 = false;
		
		std::sample(cards.begin(), cards.end(), std::back_inserter(player1), 2, gen);
		std::sample(cards.begin(), cards.end(), std::back_inserter(player2), 2, gen);
		
		std::vector<std::tuple<std::string, std::string>> vPosition;
		for (int i = 0; i < 8; i++) {
			std::uniform_int_distribution<int> dist1(0, player1.size() - 1);
			std::uniform_int_distribution<int> dist2(0, player2.size() - 1);
			
			const int random1 = dist1(gen);
			const int random2 = dist2(gen);
			
			const std::string choice1 = player1[random1];
			const std::string choice2 = player2[random2];
			player1.erase(player1.begin() + random1);
			player2.erase(player2.begin() + random2);
			
			if (choice1 == "king") {
				if (choice2 == "servant") {
					point1 += 1;
					vPosition.push_back(std::make_tuple("king", "servant"));
				} else if (choice2 == "slave") {
					point2 += 1;
					vPosition.push_back(std::make_tuple("king", "slave"));
				} else {
					vPosition.push_back(std::make_tuple("king", "king"));
				}
			} else if (choice1 == "servant") {
				if (choice2 == "king") {
					point2 += 1;
					vPosition.push_back(std::make_tuple("servant", "king"));
				} else if (choice2 == "slave") {
					point1 += 1;
					vPosition.push_back(std::make_tuple("servant", "slave"));
				} else {
					vPosition.push_back(std::make_tuple("servant", "servant"));
				}
			} else if (choice1 == "slave") {
				if (choice2 == "king") {
					point1 += 1;
					vPosition.push_back(std::make_tuple("slave", "king"));
				} else if (choice2 == "servant") {
					point2 += 1;
					vPosition.push_back(std::make_tuple("slave", "servant"));
				} else {
					vPosition.push_back(std::make_tuple("slave", "slave"));
				}
			}
			
			if (point1 >= 3) {
				state1 = true;
				break;
			} else if (point2 >= 3) {
				state2 = true;
				break;
			}
		}
		
		positions.insert(vPosition);
		
		if (state1) {
			dict["player1"] += 1;
		} else if (state2) {
			dict["player2"] += 1;
		} else {
			dict["draw"] += 1;
		}
		games += 1;
		//std::cout << "player1: " << dict["player1"]*100/games << ", player2: " << dict["player2"]*100/games << ", draw: " << dict["draw"]*100/games << '\r';
		/*for (const std::tuple<std::string, std::string> tuple : vPosition) {
			std::cout << "(" << std::get<0>(tuple) << ", " << std::get<1>(tuple) << "), ";
		}
		std::cout << '\n';*/
		std::cout << positions.size() << '\r';
		std::cout.flush();
	}
}