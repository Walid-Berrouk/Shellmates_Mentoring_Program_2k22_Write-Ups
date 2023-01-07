#include <stdlib.h>
#include <stdio.h>


//gcc challenge.c -o challenge

int main(){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    printf("Welcome to the NegativeSum challenge\n");
    
    short a,b;

    printf("a = ");
    scanf("%hd",&a);

    printf("b = ");
    scanf("%hd",&b);
    short c = a + b;
    printf("a + b = %d\n", c);
    
    // if(a>0 && b>0){
    //     short result = a+b;
    //     printf("> result = %hd\n", result);

    //     if (result == -1337){
    //         printf("Congrats Here is your flag: \n ");
    //         system("/bin/cat flag\n");
    //     } else {
    //         printf("A long way to become a 1337!\n");
    //     }
    // } else {
    //     printf("We accept only positive values!\n");
    // }
    
    return 0;
}