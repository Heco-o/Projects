#include <iostream>
#include <algorithm>
#include <unordered_map>
#include <vector>

std::vector < std::string > most_common_letter_word(std::vector < std::string>& words_list) {
	std::unordered_map < char,
	int > combined_counts;
	for (const auto& word: words_list) {
		for (const auto& letter: word) {
			++combined_counts[letter];
		}
	}

	std::sort(words_list.begin(), words_list.end(), [&](const std::string& a, const std::string& b) {
		int a_count = 0, b_count = 0;
		for (const auto& letter: a) {
			a_count += combined_counts[letter];
		}
		for (const auto& letter: b) {
			b_count += combined_counts[letter];
		}
		return a_count > b_count;
	});

	return words_list;
}
int main() {
	std::vector < std::string > words_list = {
		"example",
		"word",
		"list"
	};
	auto sorted_words = most_common_letter_word(words_list);
	for (const auto& word: sorted_words) {
		std::cout << word << ' ';
	}
	return 0;
}