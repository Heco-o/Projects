#include <cppitertools/itertools.hpp>
#include <nlohmann/json.hpp>
#include <iostream>
#include <fstream>
#include <atomic>
#include <chrono>
#include <thread>
#include <vector>

/*#include <boost/type_index.hpp>
template <typename T>
std::string type(const T& input) {
    return boost::typeindex::type_id_with_cvr<T>().pretty_name();
}*/

template<typename T, std::size_t N>
int count(const std::array<T, N>& array, const T& value) {
	int num = 0;
	for (const T& elem : array) {
		if (elem == value) {
			num++;
		}
	}
	return num;
}

void printLenPos(const std::atomic<bool>& running, const std::atomic<int>& Count) {
	while (running.load()) {
		std::cout << Count.load() << '\r' << std::flush;
	} std::this_thread::sleep_for(std::chrono::milliseconds(50));
}

void check(const std::tuple<std::string, std::string>& Tuple, std::unordered_map<std::string, int>& cards1, std::unordered_map<std::string, int>& cards2, int& point1, int& point2) {
	if (std::get<0>(Tuple) == "k") {
		if (std::get<1>(Tuple) == "k") {
			cards1["k"] -= 1;
			cards2["k"] -= 1;
		} else if (std::get<1>(Tuple) == "p") {
			point1 += 1;
			cards1["k"] -= 1;
			cards2["p"] -= 1;
		} else if (std::get<1>(Tuple) == "s") {
			point2 += 1;
			cards1["k"] -= 1;
			cards2["s"] -= 1;
		}
	} else if (std::get<0>(Tuple) == "p") {
		if (std::get<1>(Tuple) == "k") {
			point2 += 1;
			cards1["p"] -= 1;
			cards2["k"] -= 1;
		} else if (std::get<1>(Tuple) == "p") {
			cards1["p"] -= 1;
			cards2["p"] -= 1;
		} else if (std::get<1>(Tuple) == "s") {
			point1 += 1;
			cards1["p"] -= 1;
			cards2["s"] -= 1;
		}
	} else if (std::get<0>(Tuple) == "s") {
		if (std::get<1>(Tuple) == "k") {
			point1 += 1;
			cards1["s"] -= 1;
			cards2["k"] -= 1;
		} else if (std::get<1>(Tuple) == "p") {
			point2 += 1;
			cards1["s"] -= 1;
			cards2["p"] -= 1;
		} else if (std::get<1>(Tuple) == "s") {
			cards1["s"] -= 1;
			cards2["s"] -= 1;
		}
	}
	
	if (auto it = cards1.find("k"); it != cards1.end() && cards1["k"] <= 0) {
		cards1.erase(it);
	} else if (auto it = cards1.find("p"); it != cards1.end() && cards1["p"] <= 0) {
		cards1.erase(it);
	} else if (auto it = cards1.find("s"); it != cards1.end() && cards1["s"] <= 0) {
		cards1.erase(it);
	}
	
	if (auto it = cards2.find("k"); it != cards2.end() && cards2["k"] <= 0) {
		cards2.erase(it);
	} else if (auto it = cards2.find("p"); it != cards2.end() && cards2["p"] <= 0) {
		cards2.erase(it);
	} else if (auto it = cards2.find("s"); it != cards2.end() && cards2["s"] <= 0) {
		cards2.erase(it);
	}
}

std::vector<std::string> getKeys(const std::unordered_map<std::string, int>& map) {
	std::vector<std::string> keys;
	keys.reserve(map.size());
	
	for (const auto& pair : map) {
		keys.push_back(pair.first);
	}
	
	return keys;
}

int main() {
	//constexpr size_t lenth = 9;
	//auto TDcards = iter::combinations(std::vector<std::string>{"k", "p", "s"}, 2);
	constexpr size_t lenth = 36;
	auto TDcards = iter::combinations_with_replacement(std::vector<std::string>{"k", "p", "s"}, 2);
	auto TDcards1 = iter::product(TDcards, TDcards);
	std::array<std::array<std::array<std::string, 2>, 2>, lenth> defaultCards;
	int num = 0;
	for (auto it = std::begin(TDcards1); it != std::end(TDcards1); it++) {
		defaultCards[num][0][0] = std::get<0>(*it)[0];
		defaultCards[num][0][1] = std::get<0>(*it)[1];
		defaultCards[num][1][0] = std::get<1>(*it)[0];
		defaultCards[num][1][1] = std::get<1>(*it)[1];
		num++;
	}
	
	std::array<std::tuple<std::unordered_map<std::string, int>, std::unordered_map<std::string, int>, std::array<std::string, 4>>, lenth> cards;
	
	num = 0;
	for (const auto& i : defaultCards) {
		cards[num] = std::make_tuple(std::unordered_map<std::string, int>{{"k", 2 + count(i[0], std::string("k"))}, {"p", 2 + count(i[0], std::string("p"))}, {"s", 2 + count(i[0], std::string("s"))}}, std::unordered_map<std::string, int>{{"k", 2 + count(i[1], std::string("k"))}, {"p", 2 + count(i[1], std::string("p"))}, {"s", 2 + count(i[1], std::string("s"))}}, std::array<std::string, 4>{i[0][0], i[0][1], i[1][0], i[1][1]});
		num++;
	}
	
	nlohmann::json positions;
	std::atomic<bool> running = true;
	std::atomic<int> Count = 0;
	//std::atomic<int> iterate = 0;
	
	std::thread TprintLenPos(printLenPos, std::ref(running), std::ref(Count));
	
	for (const auto& card : cards) {
		//iterate++;
		auto positions1 = iter::product(std::vector<std::string>{"k", "p", "s"}, std::vector<std::string>{"k", "p", "s"});
		const std::array<std::string, 4> position0 = std::get<2>(card);
		const std::string strPosition0 = position0[0] + position0[1] + position0[2] + position0[3];
		positions[strPosition0] = {0, nlohmann::json::object()};
		for (const auto& position1 : positions1) {
			//iterate++;
			std::unordered_map<std::string, int> p1cards1 = std::get<0>(card), p2cards1 = std::get<1>(card);
			int p1point1 = 0, p2point1 = 0;
			check(position1, p1cards1, p2cards1, p1point1, p2point1);
			
			const std::string strPosition1 = std::get<0>(position1) + std::get<1>(position1);
			positions[strPosition0][1][strPosition1] = {0, nlohmann::json::object()};
			auto positions2 = iter::product(getKeys(p1cards1), getKeys(p2cards1));
			
			for (const auto& position2 : positions2) {
				//iterate++;
				std::unordered_map<std::string, int> p1cards2 = p1cards1, p2cards2 = p2cards1;
				int p1point2 = p1point1, p2point2 = p2point1;
				check(position2, p1cards2, p2cards2, p1point2, p2point2);
				
				const std::string strPosition2 = std::get<0>(position2) + std::get<1>(position2);
				positions[strPosition0][1][strPosition1][1][strPosition2] = {0, nlohmann::json::object()};
				auto positions3 = iter::product(getKeys(p1cards2), getKeys(p2cards2));
				
				for (const auto& position3 : positions3) {
					//iterate++;
					std::unordered_map<std::string, int> p1cards3 = p1cards2, p2cards3 = p2cards2;
					int p1point3 = p1point2, p2point3 = p2point2;
					check(position3, p1cards3, p2cards3, p1point3, p2point3);
					const std::string strPosition3 = std::get<0>(position3) + std::get<1>(position3);
					if (p1point3 >= 3) {
						Count++;
						positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3] = {100, nullptr};
						continue;
					} else if (p2point3 >= 3) {
						Count++;
						positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3] = {-100, nullptr};
						continue;
					} else {
						positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3] = {0, nlohmann::json::object()};
					}
					
					auto positions4 = iter::product(getKeys(p1cards3), getKeys(p2cards3));
					
					for (const auto& position4 : positions4) {
						std::unordered_map<std::string, int> p1cards4 = p1cards3, p2cards4 = p2cards3;
						int p1point4 = p1point3, p2point4 = p2point3;
						check(position4, p1cards4, p2cards4, p1point4, p2point4);
						
						const std::string strPosition4 = std::get<0>(position4) + std::get<1>(position4);
						if (p1point4 >= 3) {
							Count++;
							positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4] = {100, nullptr};
							continue;
						} else if (p2point4 >= 3) {
							Count++;
							positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4] = {-100, nullptr};
							continue;
						} else {
							positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4] = {0, nlohmann::json::object()};
						}
						
						auto positions5 = iter::product(getKeys(p1cards4), getKeys(p2cards4));
						
						for (const auto& position5 : positions5) {
							std::unordered_map<std::string, int> p1cards5 = p1cards4, p2cards5 = p2cards4;
							int p1point5 = p1point4, p2point5 = p2point4;
							check(position5, p1cards5, p2cards5, p1point5, p2point5);
							
							const std::string strPosition5 = std::get<0>(position5) + std::get<1>(position5);
							if (p1point5 >= 3) {
								Count++;
								positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5] = {100, nullptr};
								continue;
							} else if (p2point5 >= 3) {
								Count++;
								positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5] = {-100, nullptr};
								continue;
							} else {
								positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5] = {0, nlohmann::json::object()};
							}
							
							auto positions6 = iter::product(getKeys(p1cards5), getKeys(p2cards5));
							
							for (const auto& position6 : positions6) {
								std::unordered_map<std::string, int> p1cards6 = p1cards5, p2cards6 = p2cards5;
								int p1point6 = p1point5, p2point6 = p2point5;
								check(position6, p1cards6, p2cards6, p1point6, p2point6);
								
								const std::string strPosition6 = std::get<0>(position6) + std::get<1>(position6);
								if (p1point6 >= 3) {
									Count++;
									positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5][1][strPosition6] = {100, nullptr};
									continue;
								} else if (p2point6 >= 3) {
									Count++;
									positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5][1][strPosition6] = {-100, nullptr};
									continue;
								} else {
									positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5][1][strPosition6] = {0, nlohmann::json::object()};
								}
								
								auto positions7 = iter::product(getKeys(p1cards6), getKeys(p2cards6));
								
								for (const auto& position7 : positions7) {
									std::unordered_map<std::string, int> p1cards7 = p1cards6, p2cards7 = p2cards6;
									int p1point7 = p1point6, p2point7 = p2point6;
									check(position7, p1cards7, p2cards7, p1point7, p2point7);
									
									const std::string strPosition7 = std::get<0>(position7) + std::get<1>(position7);
									if (p1point7 >= 3) {
										Count++;
										positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5][1][strPosition6][1][strPosition7] = {100, nullptr};
										continue;
									} else if (p2point7 >= 3) {
										Count++;
										positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5][1][strPosition6][1][strPosition7] = {-100, nullptr};
										continue;
									} else {
										positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5][1][strPosition6][1][strPosition7] = {0, nlohmann::json::object()};
									}
									
									const std::tuple<std::string, std::string> position8 = std::make_tuple(getKeys(p1cards7)[0], getKeys(p2cards7)[0]);
									
									std::unordered_map<std::string, int> p1cards8 = p1cards7, p2cards8 = p2cards7;
									int p1point8 = p1point7, p2point8 = p2point7;
									check(position8, p1cards8, p2cards8, p1point8, p2point8);
									
									const std::string strPosition8 = std::get<0>(position8) + std::get<1>(position8);
									if (p1point8 >= 3 || p1point8 > p2point8) {
										Count++;
										positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5][1][strPosition6][1][strPosition7][1][strPosition8] = {100, nullptr};
									} else if (p2point8 >= 3 || p2point8 > p1point8) {
										Count++;
										positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5][1][strPosition6][1][strPosition7][1][strPosition8] = {-100, nullptr};
									} else {
										Count++;
										positions[strPosition0][1][strPosition1][1][strPosition2][1][strPosition3][1][strPosition4][1][strPosition5][1][strPosition6][1][strPosition7][1][strPosition8] = {0, nullptr};
									}
								}
							}
						}
					}
				}
			}
		}
	}
	//std::cout << positions.dump() << std::endl;
	running.store(false);
	TprintLenPos.join();
	std::cout << Count << std::endl;
	//std::cout << iterate << std::endl;
	std::ofstream file("positions.json");
	file << positions.dump();
	file.close();
	std::cout << "Done!" << std::endl;
}