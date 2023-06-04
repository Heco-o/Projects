#include <stdio.h>

int main(){
	char name[25];
	printf("Enter your name:\n");
	fgets(name, sizeof(name), stdin);
	printf("Your name is \"%s\"", name);
	return 0;
}