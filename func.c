/*
* This is the source file used in example for bocbor.py script 
* Output:
*
* $ gcc -o func func.c
* $ ./func
* This is function print_func
* abcdefg
* This is function print_func
* abcdefg
* This is function print_func
* abcdefg
* This is function print_func
* abcdefg
* $
*
*/
#include <stdio.h>
#include <stdlib.h>

void print_func(char * s) {
	printf("This is function print_func\n");
	printf("%s",s);
}

int main() {
	int main_a;
	int i;
	char * main_b;
	main_a=8;
	main_b="abcdefg\n";
	for (i=0; i<4; i++) {
		print_func(main_b);
	}
}
