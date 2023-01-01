# XOR 1

## Write-Up

The key to solve this challenge is knowing an interesting property of the `XOR` : is that when encrypted with a key (Xored with a key), if we Xor back the encrypted data with the same key we get the plain text !

So, since we have the key which is `simpleXor`, the only remaining thing to do is to Xor it back to get the flag.

Here are some scripts you can use to do that :

```python
#!/usr/bin/env python3

flag = b'4\x06\x02\x14L\x0f7\rRRI%\x15\x1e\x00x\x06\x01S\x10\x02\x05\x1eE>\x03\x13\x14I\x1e\x18\t\t4\x02\x13\x07\x0c\x1e\x0b\x14U*0;\x006\\=\x1c**X\x13\x1d\x1d29":\x1b\x1d\x0b\x03^"/;**^6\x0e'

key = b'simpleXor'

def encrypt(ptxt, key):
    ctxt = b''
    for i in range(len(ptxt)):
        a = ptxt[i]
        b = key[i % len(key)]
        ctxt += bytes([a ^ b])
    return ctxt

ctxt = encrypt(flag, key)

print(ctxt)
```

After Execution :

```
b'Good job ! Here is your flag shellmates{x0r_Is_1MpOr7ant_IN_Cryp7O_WOr1D}'
```

```python
#!/usr/bin/python3

from pwn import xor

flag = b'4\x06\x02\x14L\x0f7\rRRI%\x15\x1e\x00x\x06\x01S\x10\x02\x05\x1eE>\x03\x13\x14I\x1e\x18\t\t4\x02\x13\x07\x0c\x1e\x0b\x14U*0;\x006\\=\x1c**X\x13\x1d\x1d29":\x1b\x1d\x0b\x03^"/;**^6\x0e'

key = b'simpleXor'

ctxt = xor(flag, key)

print(ctxt)
```

After Execution :

```
b'Good job ! Here is your flag shellmates{x0r_Is_1MpOr7ant_IN_Cryp7O_WOr1D}'
```

**Note :** The decryption is the encryption itself (Which is a Xor), we can use also xor method from pwn.


## Flag

shellmates{x0r_Is_1MpOr7ant_IN_Cryp7O_WOr1D}

## More Information