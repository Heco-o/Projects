#include <iostream>
#include <vector>

class A {
	public:
	std::string name = "name";
	int num = 100;
};

class B : public A {
	public:
	int bad = 5;
	int ok = 10;
};

int main() {
	std::vector<A> vec;
	B a;
	vec.push_back(a);
	std::cout << vec[0].name << std::endl;
	std::cout << vec[0].num << std::endl;
	std::cout << vec[0].bad << std::endl;
	std::cout << vec[0].ok << std::endl;
}