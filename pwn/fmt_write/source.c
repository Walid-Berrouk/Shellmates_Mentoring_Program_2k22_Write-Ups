#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NAME_LEN 50

// gcc -m32 -o chall source.c

void disable_buffering() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int main(void) {
    
    disable_buffering();

    int authenticated = 0;
    printf("This may help later : 0x%x\n", &authenticated);

    char name[NAME_LEN];
    
    printf("Name : ");
    fgets(name, NAME_LEN, stdin);
    
    printf("Hi, ");
    printf(name);

    printf("[authenticated] = %d\n", authenticated);

    if (authenticated == 1)
        printf("shellmates{XXXXXXXXXXXXXXXXXXXXX}\n");
    else 
        printf("Nope! You won't be getting any flags\n");

    return 0;
}
