#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAG_LEN 34
#define NAME_LEN 50

// gcc  -Wl,-z,relro,-z,now -m32 -o chall source.c

void disable_buffering() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int main(void) {
    
    disable_buffering();

    char *flag = (char*) malloc(sizeof(char)*FLAG_LEN);
    memcpy(flag, "shellmates{XXXXXXXXXXXXXXXXXXXXX}", FLAG_LEN);
    printf("This may help later : 0x%x\n",flag);

    char name[NAME_LEN];
    
    printf("Name : ");
    fgets(name, NAME_LEN, stdin);
    
    printf("Hi, ");
    printf(name);
    
    free(flag);
    
    return 0;
}
