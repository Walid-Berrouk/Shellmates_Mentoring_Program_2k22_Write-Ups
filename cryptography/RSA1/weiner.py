#! /usr/bin/python3

from Crypto.Util.number import *
import owiener

f = open('RSA1.txt', 'r')
e = int(f.readline().split("=")[1].strip())
n = int(f.readline().split("=")[1].strip())
c = int(f.readline().split("=")[1].strip())

# Decryption with weiner Attack
d = owiener.attack(e, n)

if d is None:
    print("Failed")
else:
    print("Hacked d={}".format(d))
    flag = long_to_bytes(pow(c, d, n))
    print(f"Decrypted flag : {flag}")  