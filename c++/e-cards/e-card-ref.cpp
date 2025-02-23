#include <nlohmann/json.hpp>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <vector>
#include <cctype>
#include <tuple>

std::ifstream file("data.json");
nlohmann::json data;

const std::vector<std::string> cards = {"king", "servant", "slave"};
std::vector<std::string> p1cards = {"king", "king", "servant", "servant", "slave", "slave"};
std::vector<std::string> p2cards = {"king", "king", "servant", "servant", "slave", "slave"};
std::string gameMsg;
std::string player1ID;
std::string player2ID;
std::string cPlayer1ID;
std::string cPlayer2ID;
std::string cPlayersID;
int playRound = 0;
int gameRound = 0;
int p1point = 0;
int p2point = 0;
bool set = false;

void saveData() {
	std::ofstream file("data.json");
	file << std::setw(4) << data;
	file.close();
}

bool isNumber(const std::string& str) {
	for (const char c : str) {
		if (!std::isdigit(c)) {
			return false;
		}
	}
	return true;
}

std::vector<std::string> split(const std::string& str) {
	std::vector<std::string> tokens;
	std::stringstream ss(str);
	std::string token;
	
	while (ss >> token) {
		tokens.push_back(token);
	}
	
	return tokens;
}

void makeGameMsg(std::string choice1, std::string choice2) {
	//if (type == "roundDraw") {
	gameMsg = "Round: " + std::to_string(playRound + 1) + "\n" \
			  "<@" + cPlayer1ID + "> placed the " + choice1 + " card.\n" \
			  "<@" + cPlayer2ID + "> placed the " + choice2 + " card.\n\n" \
			  + std::to_string(p1point) + " - " + std::to_string(p2point);
	//}
	system(("termux-clipboard-set \"" + gameMsg + "\"").c_str());
}

void check(std::string choice1, std::string choice2) {
	if (choice1 == "king") {
		if (choice2 == "king") {
			makeGameMsg(choice1, choice2);
			data[cPlayersID]["games"][gameRound]["game"].push_back({"king", "king"});
		} else if (choice2 == "servant") {
			p1point += 1;
			makeGameMsg(choice1, choice2);
			data[cPlayersID]["games"][gameRound]["game"].push_back({"king", "servant"});
		} else if (choice2 == "slave") {
			p2point += 1;
			makeGameMsg(choice1, choice2);
			data[cPlayersID]["games"][gameRound]["game"].push_back({"king", "slave"});
		}
	} else if (choice1 == "servant") {
		if (choice2 == "king") {
			p2point += 1;
			makeGameMsg(choice1, choice2);
			data[cPlayersID]["games"][gameRound]["game"].push_back({"servant", "king"});
		} else if (choice2 == "servant") {
			makeGameMsg(choice1, choice2);
			data[cPlayersID]["games"][gameRound]["game"].push_back({"servant", "servant"});
		} else if (choice2 == "slave") {
			p1point += 1;
			makeGameMsg(choice1, choice2);
			data[cPlayersID]["games"][gameRound]["game"].push_back({"servant", "slave"});
		}
	} else if (choice1 == "slave") {
		if (choice2 == "king") {
			p1point += 1;
			makeGameMsg(choice1, choice2);
			data[cPlayersID]["games"][gameRound]["game"].push_back({"slave", "king"});
		} else if (choice2 == "servant") {
			p2point += 1;
			makeGameMsg(choice1, choice2);
			data[cPlayersID]["games"][gameRound]["game"].push_back({"slave", "servant"});
		} else if (choice2 == "slave") {
			makeGameMsg(choice1, choice2);
			data[cPlayersID]["games"][gameRound]["game"].push_back({"slave", "slave"});
		}
	}
	if (!p1cards.empty()) {
		p1cards.erase(std::find(p1cards.begin(), p1cards.end(), choice1));
	} if (!p2cards.empty()) {
		p2cards.erase(std::find(p2cards.begin(), p2cards.end(), choice2));
	}
	
	data[cPlayersID]["games"][gameRound]["info"]["player1Cards"] = p1cards;
	data[cPlayersID]["games"][gameRound]["info"]["player2Cards"] = p2cards;
	data[cPlayersID]["games"][gameRound]["info"]["player1point"] = p1point;
	data[cPlayersID]["games"][gameRound]["info"]["player2point"] = p2point;
}

void checkPoint() {
	if (p1point >= 3) {
		gameRound += 1;
		data[cPlayersID]["info"]["games"] = data[cPlayersID]["games"].size();
		data[cPlayersID]["info"]["draft"] = false;
		std::cout << "\nPlayer1 has won the game!" << std::flush;
		p1cards = {"king", "king", "servant", "servant", "slave", "slave"};
		p2cards = {"king", "king", "servant", "servant", "slave", "slave"};
		p1point = 0;
		p2point = 0;
	} else if (p2point >= 3) {
		gameRound += 1;
		data[cPlayersID]["info"]["games"] = data[cPlayersID]["games"].size();
		data[cPlayersID]["info"]["draft"] = false;
		std::cout << "\nPlayer2 has won the game!" << std::flush;
		p1cards = {"king", "king", "servant", "servant", "slave", "slave"};
		p2cards = {"king", "king", "servant", "servant", "slave", "slave"};
		p1point = 0;
		p2point = 0;
	} else if (playRound >= 7 || p1cards.size() <= 0 && p2cards.size() <= 0) {
		gameRound += 1;
		data[cPlayersID]["info"]["games"] = data[cPlayersID]["games"].size();
		data[cPlayersID]["info"]["draft"] = false;
		std::cout << "\nThe game is a draw!" << std::flush;
		p1cards = {"king", "king", "servant", "servant", "slave", "slave"};
		p2cards = {"king", "king", "servant", "servant", "slave", "slave"};
		p1point = 0;
		p2point = 0;
	}
}

void info() {
	std::cout << "Player1 Point: " << p1point << std::endl;
	std::cout << "Player2 Point: " << p2point << std::endl;
	std::cout << "Player1 Cards: " << std::flush;
	for (const std::string i : p1cards) {
		std::cout << i << ", " << std::flush;
	}
	std::cout << "\nPlayer2 Cards: " << std::flush;
	for (const std::string i : p2cards) {
		std::cout << i << ", " << std::flush;
	}
	if (set && data[cPlayersID]["info"]["draft"]) {
		std::cout << "\nplayRound: " << playRound + 1 << ", gameRound: " << gameRound + 1 << std::endl;
		std::cout << "Cards Placed -> Player1, Player2: " << data[cPlayersID]["games"][gameRound]["game"][playRound].dump() << std::flush;
	} else {
		std::cout << "\nplayRound: " << 0 << ", gameRound: " << gameRound + 1 << std::endl;
		std::cout << "Cards Placed -> Player1, Player2: " << "[null, null]" << std::flush;
		
	}
}

int main() {
	if (!file.is_open()) {
		std::cerr << "Failed to open file!";
		return 1;
	} 

	try {
		file >> data;
		file.close();
	} catch (const std::exception& e) {
		std::cerr << "Failed to parse JSON.\n" << e.what();
		return 1;
	}
	
	while (true) {
		std::string command;
		std::cout << "E-Card[>] "  << std::flush;
		std::getline(std::cin, command);
		const std::vector<std::string> commands = split(command);
		const size_t size = commands.size();
		
		if (size > 0) {
			if (commands[0] == "p1id") {
				if (size > 1) {
					if (isNumber(commands[1])) {
						player1ID = commands[1];
						std::cout << "Player1 ID: " << player1ID << std::flush;
					} else {
						std::cout << "Please enter a valid id." << std::flush;
					}
				} else {
					std::cout << "Please enter an ID" << std::flush;
				}
			} else if (commands[0] == "p2id") {
				if (size > 1) {
					if (isNumber(commands[1])) {
						player2ID = commands[1];
						std::cout << "Player2 ID: " << player2ID << std::flush;
					} else {
						std::cout << "Please enter a valid id." << std::flush;
					}
				} else {
					std::cout << "Please enter an ID" << std::flush;
				}
			} else if (commands[0] == "add1" && size > 1) {
				for (int i = 1; i < size; i++) {
					if (std::find(cards.begin(), cards.end(), commands[i]) != cards.end()) {
						p1cards.push_back(commands[i]);
						std::cout << commands[i] << " has been added to player1's cards." << std::endl;
					} else {
						std::cout << "'" << commands[i] << "' isn't a valid card." << std::endl;
					}
				}
			} else if (commands[0] == "add2" && size > 1) {
				for (int i = 1; i < size; i++) {
					if (std::find(cards.begin(), cards.end(), commands[i]) != cards.end()) {
						p2cards.push_back(commands[i]);
						std::cout << commands[i] << " has been added to player2's cards." << std::endl;
					} else {
						std::cout << "'" << commands[i] << "' isn't a valid card." << std::endl;
					}
				}
			} else if (commands[0] == "sub1" && size > 1) {
				for (int i = 1; i < size; i++) {
					if (std::find(cards.begin(), cards.end(), commands[i]) != cards.end()) {
						std::vector<std::string>::iterator it = std::find(p1cards.begin(), p1cards.end(), commands[i]);
						if (it != p1cards.end()) {
							p1cards.erase(it);
							std::cout << commands[i] << " has been removed from player1's cards." << std::endl;
						} else {
							std::cout << "Player1 doesn't have any " << commands[i] << " cards." << std::endl;
						}
					} else {
						std::cout << "'" << commands[i] << "' isn't a valid card." << std::endl;
					}
				}
			} else if (commands[0] == "sub2" && size > 1) {
				for (int i = 1; i < size; i++) {
					if (std::find(cards.begin(), cards.end(), commands[i]) != cards.end()) {
						std::vector<std::string>::iterator it = std::find(p2cards.begin(), p2cards.end(), commands[i]);
						if (it != p2cards.end()) {
							p2cards.erase(it);
							std::cout << commands[i] << " has been removed from player2's cards." << std::endl;
						} else {
							std::cout << "Player2 doesn't have any " << commands[i] << " cards." << std::endl;
						}
					} else {
						std::cout << "'" << commands[i] << "' isn't a valid card." << std::endl;
					}
				}
			} else if (commands[0] == "set") {
				if (player1ID != "" && player2ID != "") {
					if (!data[player1ID + ", " + player2ID].is_null()) {
						cPlayer1ID = player1ID;
						cPlayer2ID = player2ID;
						cPlayersID = player1ID + ", " + player2ID;
						if (data[cPlayersID]["info"]["draft"]) {
							std::string input;
							std::cout << "A game was unfinished with these players.\nDo you want to continue from there?\n[y/n]->;" << std::flush;
							std::cin >> input;
							if (std::tolower(input[0]) == 'y') {
								set = true;
								gameRound = data[cPlayersID]["games"].size() - 1;
								playRound = data[cPlayersID]["games"][gameRound]["game"].size() - 1;
								p1cards = data[cPlayersID]["games"][gameRound]["info"]["player1Cards"];
								p2cards = data[cPlayersID]["games"][gameRound]["info"]["player2Cards"];
								p1point = data[cPlayersID]["games"][gameRound]["info"]["player1point"];
								p2point = data[cPlayersID]["games"][gameRound]["info"]["player2point"];
								std::cout << "The game will continue from where it left off." << std::flush;
							} else {
								set = true;
								p1point = 0;
								p2point = 0;
								p1cards = {"king", "king", "servant", "servant", "slave", "slave"};
								p2cards = {"king", "king", "servant", "servant", "slave", "slave"};
								gameRound = data[cPlayersID]["games"].size();
								data[cPlayersID]["info"]["games"] = data[cPlayersID]["games"].size();
								data[cPlayersID]["info"]["draft"] = false;
								std::cout << "A new game will be played." << std::flush;
							}
						} else {
							set = true;
							p1point = 0;
							p2point = 0;
							p1cards = {"king", "king", "servant", "servant", "slave", "slave"};
							p2cards = {"king", "king", "servant", "servant", "slave", "slave"};
							gameRound = data[cPlayersID]["games"].size();
							data[cPlayersID]["info"]["games"] = data[cPlayersID]["games"].size();
							std::cout << "A new game will be played." << std::flush;
						}
					} else {
						set = true;
						p1point = 0;
						p2point = 0;
						p1cards = {"king", "king", "servant", "servant", "slave", "slave"};
						p2cards = {"king", "king", "servant", "servant", "slave", "slave"};
						cPlayer1ID = player1ID;
						cPlayer2ID = player2ID;
						cPlayersID = player1ID + ", " + player2ID;
						data[cPlayersID]["info"]["player1ID"] = std::stoll(player1ID);
						data[cPlayersID]["info"]["player2ID"] = std::stoll(player2ID);
						data[cPlayersID]["info"]["games"] = 0;
						data[cPlayersID]["info"]["draft"] = false;
						data[cPlayersID]["games"] = nlohmann::json::array();
						
						saveData();
						std::cout << "A new game will be played." << std::flush;
					}
				} else {
					std::cout << "Please set both player's id first." << std::flush;
				}
			
			} else if (commands[0] == "next") {
				if (size >= 3) {
					bool pass = false;
					if (std::find(cards.begin(), cards.end(), commands[1]) != cards.end()) {
						if (std::find(cards.begin(), cards.end(), commands[2]) != cards.end()) {
							if (std::find(p1cards.begin(), p1cards.end(), commands[1]) != p1cards.end()) {
								if (std::find(p2cards.begin(), p2cards.end(), commands[2]) != p2cards.end()) {
									if (set) {
										pass = true;
									} else {
										std::cout << "Please set the game first." << std::flush;
									}
								} else {
									std::cout << "Player2 doesn't have any " + commands[2] + "cards." << std::flush;
								}
							} else {
								std::cout << "player1 doesn't have any " + commands[1] + " cards." << std::flush;
							}
						} else {
							std::cout << "There is no card named '" << commands[2] << "'." << std::flush;
						}
					} else {
						std::cout << "There is no card named '" << commands[1] << "'." << std::flush;
					}
					if (pass) {
						if (!data[cPlayersID]["info"]["draft"]) {
							data[cPlayersID]["info"]["draft"] = true;
							playRound = 0;
							data[cPlayersID]["games"].push_back(nlohmann::json::object({
								{"game", nlohmann::json::array()},
								{"info", nlohmann::json::object()}
							}));
							check(commands[1], commands[2]);
							info();
							saveData();
						} else {
							playRound += 1;
							check(commands[1], commands[2]);
							info();
							checkPoint();
							saveData();
						}
					}
				}
			} else if (commands[0] == "copy") {
				system(("termux-clipboard-set \"" + gameMsg + "\"").c_str());
			} else if (commands[0] == "save") {
				saveData();
			} else if (commands[0] == "json") {
				std::cout << data.dump();
			} else if (commands[0] == "info") {
				info();
			} else if (commands[0] == "exit") {
				break;
			} else {
				std::cout << "Unknown command." << std::flush;
			}
		}
		std::cout << std::endl;
	}
	saveData();
}