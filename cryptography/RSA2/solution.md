# itsybitsyrsa

## Write-Up

When we annalyse the values of rsa, we can see that we have a small `e` value with a too big `n` value.

Our main reflex is to try an attack on rsa when the `e` value is too small. Basically, here is how the ciphertext is formed :

<img src="./enc.svg" alt="RSA Encryption" style="background-color: white;"/>

As we can see, and since the `n` value is too big, the mod will basically return the same value. So, to decrypt the message, the only thing to do is to do the `e`th root of the ciphertext.

you can see the code exploit here :

```python
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
```

**Note :** In this case, we can use the `sqrt` to decrypt the flag, but with `iroot` it is a general solution for any `e`

And here is the output :

```
b'shellmates{4v0id_5m4ll_3xp0n3nt5}' is a true root
shellmates{4v0id_5m4ll_3xp0n3nt5}
```

## Flag

shellmates{4v0id_5m4ll_3xp0n3nt5}

## More information

https://en.wikipedia.org/wiki/RSA_(cryptosystem)
https://www.johndcook.com/blog/2019/03/06/rsa-exponent-3/   