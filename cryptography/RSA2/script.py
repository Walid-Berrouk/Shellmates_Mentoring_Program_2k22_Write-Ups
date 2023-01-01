#! /usr/bin/python3

from Crypto.Util.number import *
from gmpy2 import iroot

# e value
f = open('RSA2.txt', 'r')
e = int(f.readline().split("=")[1].strip())
n = int(f.readline().split("=")[1].strip())
c = int(f.readline().split("=")[1].strip())

output = long_to_bytes(int(iroot(c, e)[0]))
print(output, end="")
if iroot(c,e)[1] == True : print(" is a true root")
else : print (" is an approximate root")
flag = str(output).strip("b'")
print(flag)