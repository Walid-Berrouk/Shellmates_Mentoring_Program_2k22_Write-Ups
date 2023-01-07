# NegativeSum 

## Description

> We learned that the sum of two positives gives a positive. This rule is no longer valid here

## Tags

integer overflow

## Write-Up

Given the following `C` code :

```c
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
    
    if(a>0 && b>0){
        short result = a+b;
        printf("> result = %hd\n", result);

        if (result == -1337){
            printf("Congrats Here is your flag: \n ");
            system("/bin/cat flag\n");
        } else {
            printf("A long way to become a 1337!\n");
        }
    } else {
        printf("We accept only positive values!\n");
    }
    
    return 0;
}
```

And from the Tags and title, we ca see that there is an **Integer Overflow** Vulnerability, so let's try to exploit that by entering the right two `positive` integers to get the negative some (Note the type of the variables used which is `short`, this last is `2 bytes` long and goes frim `-32,768` to `32,767`):

```
Welcome to the NegativeSum challenge
a = 32766
b = 31433
a + b = -1337
```

If you are wondering how i got the number, it is easy :

 - First, you have got to overflow one of the variables, and then enter the result wanted in the second one :

```
Welcome to the NegativeSum challenge
a = 32768
b = 1337
a + b = -31431
```

 - After that, just switch between the result and wanted result (Don't forget to compensate to make the values positive, since `32768` will overflow the first variable and turn it into a negative one) :

```
Welcome to the NegativeSum challenge
a = 32766
b = 31433
-1337
```

Now, let's connect to our instance and get the flag using these numbers :

```
Welcome to the NegativeSum challenge
a = 32766
b = 31433
> result = -1337
Congrats Here is your flag: 
 shellmates{1_10v3_1nt3ger_0v3rF10w}

```


## Flag

shellmates{1_10v3_1nt3ger_0v3rF10w}

## More Information

 - Integer overflow :
   - https://en.wikipedia.org/wiki/Integer_overflow
   - https://www.welivesecurity.com/2022/02/21/integer-overflow-how-it-occur-can-be-prevented/
 - C Data types : https://www.tutorialspoint.com/cprogramming/c_data_types.htm
