from Crypto.Util.number import *

f = open('RSA0.txt', 'r')
n = int(f.readline().split("=")[1].strip())
p = int(f.readline().split("=")[1].strip())
q = int(f.readline().split("=")[1].strip())
e = int(f.readline().split("=")[1].strip())
enc = int(f.readline().split("=")[1].strip())


d = pow(e, -1, (p-1)*(q-1))

flag = pow(enc, d, n)
flag = long_to_bytes(flag)

print(flag)