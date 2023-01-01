#! /usr/bin/python3

from Crypto.Util.number import *

f = open('RSA1.txt', 'r')
e = int(f.readline().split("=")[1].strip())
n = int(f.readline().split("=")[1].strip())
enc = int(f.readline().split("=")[1].strip())

# After Factorization
p = 9942874965373398689
q = 102411157768469768587484356311902427789461430190314198242306101223897141593967

d = pow(e, -1, (p-1)*(q-1))

flag = pow(enc, d, n)
flag = long_to_bytes(flag)

print(flag)
