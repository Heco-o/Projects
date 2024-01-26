#include <iostream>

int main(){
	int n;
	std::cout << "Enter the size of the squre" << std::endl;
	std::cin >> n;
	
	for(int i = 0; n > i; i++){
		for(int j = 0; n > j; j++){
			std::cout << "#";
		}
		std::cout << std::endl;
	}
}