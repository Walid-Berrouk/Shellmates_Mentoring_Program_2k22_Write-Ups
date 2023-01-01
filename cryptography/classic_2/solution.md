# Classic 2

## Write-Up

When checking attachments of the challenge, we can find two files :
 
 - `enc` : contains encrypted flag
 - `challenge.py` :  contains encryption program for the flag

Seeing closer the program, we can see that depending on a key value, it is actually making a rotation on a set of alphabets that contains letters and digits. its length is `62`.

So, in order for us to recover the flag, we need to do the symetric rotation of the one done in the program, but this time mod `62` and `not 26` like in usual `rot` or `caesar` encryption.

First of all, we need to recover the key. To do that, we shall use one character of the encrypted flag that we actually know the real value :

 - First character of the flag like the flag format says is `s`
 - In the encrypted flag, it is replaced by a `J`

So, after getting index of each in the set of alphabet, a simple substraction may do the work :


```py

In [1]: import string

In [2]: possible_chars = string.ascii_letters + string.digits

In [3]: print(possible_chars)
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789

In [4]: possible_chars.index('s')
Out[4]: 18

In [5]: possible_chars.index('J')
Out[5]: 35

```

So we have (From program) : 

(18 + key) % 62 = 35

Then the key is : 

35 - 18 = 17

So, the key is `17`

Now, in order to recover the flag, we need to do the symetric rotation in the `62` long alphabet. Which gives us :

62 - 17 = 45

So we need to apply a rotation by `45` characters to do the decryption. To do that, we can either :

 - Use same script with change of the key to `45` :

```python
import string

f = open('enc', 'r')

key = 45
flag = f.read()

possible_chars = string.ascii_letters + string.digits
n = len(possible_chars)
dec = ''

for c in flag :
    if c in possible_chars :
        i =  possible_chars.index(c)
        dec += possible_chars[(i + key) % n]
    else :
        dec += c

print(dec)
```

```
Output : 
shellmates{bRutEF0rc3_MaY_com3_h4Ndy}
```

 - Use Generic decryption function :




```py
In [7]: def rot(*symbols):
   ...:     def _rot(n):
   ...:         encoded = ''.join(sy[n:] + sy[:n] for sy in symbols)
   ...:         lookup = str.maketrans(''.join(symbols), encoded)
   ...:         return lambda s: s.translate(lookup)
   ...:     return _rot
   ...: 

In [10]: import string

In [11]: possible_chars = string.ascii_letters + string.digits

In [12]: rot_alpha = rot(possible_chars)

In [25]: rot45_alpha_enc = rot_alpha(45)

In [26]: rot45_alpha_enc('JyvCCDrKvJ{s8LKVWhItk_3rf_tFDk_yl4uP}')
Out[26]: 'shellmates{bRutEF0rc3_MaY_com3_h4Ndy}'

# Or sideways :

In [25]: rot17_alpha_dec = rot_alpha(-17)

In [26]: rot17_alpha_dec('JyvCCDrKvJ{s8LKVWhItk_3rf_tFDk_yl4uP}')
Out[26]: 'shellmates{bRutEF0rc3_MaY_com3_h4Ndy}'

```

## Flag

shellmates{bRutEF0rc3_MaY_com3_h4Ndy}

## More Information

https://eddmann.com/posts/implementing-rot13-and-rot-n-caesar-ciphers-in-python/

rot 13 and all the others : https://rot13.com/
