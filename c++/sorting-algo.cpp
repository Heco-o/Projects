#include <iostream>
#include <type_traits>
#include <list>
#include <forward_list>
#include <vector>
#include <deque>
#include <array>
#include <random>
#include <algorithm>
#include <boost/type_index.hpp>

std::random_device rd;
std::mt19937 rng(rd());

template<typename T>
void bubbleSort(T& array) {
	size_t size = std::size(array) - 1;
	while (size != 0) {
		for (size_t i = 0; i < size; ++i) {
			if (array[i] > array[i + 1]) {
				std::swap(array[i], array[i + 1]);
			}
		} --size;
	}
}

template<typename T>
void bubbleSortP(T& array) {
	auto begin = std::begin(array);
	auto end = std::prev(std::end(array));
	while (begin != end) {
		for (auto i = begin; i != end; ++i) {
			if (*i > *std::next(i)) {
				std::swap(*i, *std::next(i));
			}
		} --end;
	}
}

template<typename T>
void insertionSort(T& array) {
	//using U = typename std::remove_reference<decltype(*std::begin(array))>::type;
	const size_t size = std::size(array);
	for (size_t i = 1; i < size; ++i) {
		const auto current = array[i];
		size_t j = i;
		while (j > 0 && array[j - 1] > current) {
			array[j] = array[j - 1];
			--j;
		} array[j] = current;
	}
}

template<typename T>
void insertionSortP(T& array) {
	auto begin = std::begin(array);
	auto end = std::end(array);
	for (auto i = std::next(begin); i != end; ++i) {
		const auto current = *i;
		auto j = i;
		while (j != begin && *std::prev(j) > current) {
			*j = *std::prev(j);
			--j;
		} *j = current;
	}
}

template<typename T>
void selectionSort(T& array) {
	const size_t size = std::size(array);
	for (size_t i = 0; i < size - 1; ++i) {
		size_t s = i;
		for (size_t j = i + 1; j < size; ++j) {
			if (array[s] > array[j]) {
				s = j;
			}
		} std::swap(array[i], array[s]);
	}
}

template<typename T>
void selectionSortP(T& array) {
	auto begin = std::begin(array);
	auto end = std::end(array);
	for (auto i = begin; i != std::prev(end); ++i) {
		auto s = i;
		for (auto j = std::next(i); j != end; ++j) {
			if (*s > *j) {
				s = j;
			}
		} std::swap(*i, *s);
	}
}

template<typename T>
void cocktailShakerSort(T& array) {
	size_t begin = 0;
	size_t end = std::size(array) - 1;
	bool swapped;
	do {
		swapped = false;
		for (size_t i = begin; i < end; ++i) {
			if (array[i] > array[i + 1]) {
				std::swap(array[i], array[i + 1]);
				swapped = true;
			}
		} if (!swapped) {
			break;
		} swapped = false;
		for (size_t i = end; i > begin; --i) {
			if (array[i - 1] > array[i]) {
				std::swap(array[i - 1], array[i]);
				swapped = true;
			}
		} ++begin;
		--end;
	} while (swapped);
}

template<typename T>
void cocktailShakerSortP(T& array) {
	auto begin = std::begin(array);
	auto end = std::prev(std::end(array));
	bool swapped;
	do {
		swapped = false;
		for (auto i = begin; i != end; ++i) {
			if (*i > *std::next(i)) {
				std::swap(*i, *std::next(i));
				swapped = true;
			}
		} if (!swapped) {
			break;
		} swapped = false;
		for (auto i = end; i != begin; --i) {
			if (*std::prev(i) > *i) {
				std::swap(*std::prev(i), *i);
				swapped = true;
			}
		} ++begin;
		--end;
	} while (swapped);
}

template<typename T>
void gnomeSort(T& array) {
	const size_t size = std::size(array);
	size_t pos = 0;
	while (pos < size) {
		if (pos == 0 || array[pos - 1] <= array[pos]) {
			++pos;
		} else {
			std::swap(array[pos - 1], array[pos]);
			--pos;
		}
	}
}

template<typename T>
void gnomeSortP(T& array) {
	auto begin = std::begin(array);
	auto end = std::end(array);
	auto current = begin;
	while (current != end) {
		if (current == begin || *std::prev(current) <= *current) {
			++current;
		} else {
			std::swap(*std::prev(current), *current);
			--current;
		}
	}
}

template<typename T>
void combSort(T& array, float shrinkFactor = 1.3) {
	const size_t size = std::size(array);
	int gap = size;
	bool swapped;
	do {
		gap = std::max(1, static_cast<int>(gap / shrinkFactor));
		swapped = false;
		for (size_t i = 0; i < size - gap; ++i) {
			if (array[i] > array[i + gap]) {
				std::swap(array[i], array[i + gap]);
				swapped = true;
			}
		}
	} while (gap != 1 || swapped);
}

template<typename T>
void combSortP(T& array, float shrinkFactor = 1.3) {
	auto begin = std::begin(array);
	auto end = std::end(array);
	bool swapped;
	int gap = std::distance(begin, end);
	do {
		swapped = false;
		gap = std::max(1, static_cast<int>(gap / shrinkFactor));
		auto j = begin;
		std::advance(j, gap);
		for (auto i = begin; j != end; ++i) {
			if (*i > *j) {
				std::swap(*i, *j);
				swapped = true;
			}
			++j;
		}
	} while (gap != 1 || swapped);
}

template<typename T>
void mergeSort(T& array) {
	const size_t size = std::size(array);
	if (size <= 1) {
		return;
	}
	
	const size_t leftSize = size / 2;
	const size_t rightSize = size - leftSize;
	
	const auto begin = std::begin(array);
	const auto mid = begin + leftSize;
	std::vector left(begin, mid);
	std::vector right(mid, std::end(array));
	
	mergeSort(left);
	mergeSort(right);
	
	size_t i = 0, j = 0, k = 0;
	while (i < leftSize && j < rightSize) {
		if (left[i] < right[j]) {
			array[k++] = left[i++];
		} else {
			array[k++] = right[j++];
		}
	} while (i < leftSize) {
		array[k++] = left[i++];
	} while (j < rightSize) {
		array[k++] = right[j++];
	}
}

template<typename InputIt>
void mergeSort(InputIt begin, InputIt end) {
	const size_t size = std::distance(begin, end);
	
	if (size <= 1) {
		return;
	}
	
	const size_t leftSize = size / 2;
	const size_t rightSize = size - leftSize;
	
	const InputIt mid = std::next(begin, leftSize);
	std::vector left(begin, mid);
	std::vector right(mid, end);
	
	mergeSort(left.begin(), left.end());
	mergeSort(right.begin(), right.end());
	
	InputIt current = begin;
	size_t i = 0, j = 0;
	while (i < leftSize && j < rightSize) {
		if (left[i] < right[j]) {
			*current++ = left[i++];
		} else {
			*current++ = right[j++];
		}
	} while (i < leftSize) {
		*current++ = left[i++];
	} while (j < rightSize) {
		*current++ = right[j++];
	}
}

template<bool randomAccess = false, typename T = int, typename U>
void test(U& array, const std::string type) {
	std::cout << type << ":" << std::endl;
	for (const T& i : array) {
		std::cout << i << ", ";
	} std::cout << std::endl;
	
	if constexpr (randomAccess) {
		mergeSort(array);
	} else {
		mergeSort(std::begin(array), std::end(array));
	}
	
	for (const T& i : array) {
		std::cout << i << ", ";
	} std::cout << std::endl << std::endl;
}

int main() {
	int arr[10] = {9,8,7,6,5,4,3,2,1,0};
	std::array<int, 10> array;
	
	std::shuffle(std::begin(arr), std::end(arr), rng);
	
	std::copy(std::begin(arr), std::end(arr), std::begin(array));
	
	std::vector<int> vector(std::begin(arr), std::end(arr));
	std::deque<int> deque(std::begin(arr), std::end(arr));
	std::list<int> list(std::begin(arr), std::end(arr));
	std::forward_list<int> forward_list(std::begin(arr), std::end(arr));
	
	test<true>(arr, "int[10]");
	test<true>(array, "std::array<int, 10>");
	test<true>(vector, "std::vector<int>");
	test(deque, "std::deque<int>");
	test(list, "std::list<int>");
	test(forward_list, "std::forward_list<int>");
}