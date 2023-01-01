# TITLE

## Description

> In order to get rid of a special message and make it unrecoverable, I encrypted it using "randomly" shuffled characters

## Tags

PRNG, Substitution

## Write-Up

After checking the `challenge.py` and from the tags, we can see that the encryption here is based on generating a random number or seed that, from this number, a list of characters that represents our encryption alphabet is being shuffled, and after that, with a substitution mechanism, used to encrypt the flag (the encrypted flag is given at the end of the file) :

```py
import random
from string import ascii_lowercase, digits
from secret import flag

chars = ascii_lowercase + digits

random.seed(2 ** 1337 - 1)

shuffled_chars = [i for i in chars]
random.shuffle(shuffled_chars)
shuffled_chars = "".join(shuffled_chars)
# print(f"{chars}\n{''.join(shuffled_chars)}");input()

enc = ""
for i in flag:
    if i.isalnum():
        enc += shuffled_chars[chars.index(i)]
    else:
        enc += i

print(enc)
#  ctn44vmunc{3ghgsy_uto_coo2_gc_2asyoxg1ec}
```

From our study of `PRNGs` and more precisely the generator function `random.seed()`, we can find that if you use the same seed value twice you will get the same random number twice. See example below (`random.random()` to print out the seed value) :

```py
import random
from string import ascii_lowercase, digits
from secret import flag

chars = ascii_lowercase + digits

random.seed(2 ** 1337 - 1)
print(random.random())
```

Results on multiple executions :

```
$ ./decrypt.py
0.5181031964987092

$ ./decrypt.py
0.5181031964987092

$ ./decrypt.py
0.5181031964987092
```

So, now we know for sure that since the seed value is a fixed value, we will have the same random number as the author used to encrypt the flag.

As for the substitution part, in order to decrypt the flag, we need only to inverse between the chars list and the chars substitution list in our code, since the decryption will consist of looking back the indexes of chars from the substitution list :

```py
...
dec += chars[shuffled_chars.index(i)]
...
```

Here is the final code :

```py
#! /usr/bin/python3

import random
from string import ascii_lowercase, digits

flag_enc = 'ctn44vmunc{3ghgsy_uto_coo2_gc_2asyoxg1ec}'

chars = ascii_lowercase + digits

random.seed(2 ** 1337 - 1)


shuffled_chars = [i for i in chars]
random.shuffle(shuffled_chars)
shuffled_chars = "".join(shuffled_chars)
# print(f"{chars}\n{''.join(shuffled_chars)}");input()

dec = ""
for i in flag_enc:
    if i.isalnum():
        dec += chars[shuffled_chars.index(i)]
    else:
        dec += i

print(dec)
```

The decryption of it will get us the flag back :

```
shellmates{f1x1ng_th3_s33d_1s_d4ng3r10us}
```

**Note :** Note the chars list and substitution char list when printing them together :

```
abcdefghijklmnopqrstuvwxyz0123456789
mr02n3ytwjl4vsd6qxcue5kh981gfoazipb7
```

## Flag

shellmates{f1x1ng_th3_s33d_1s_d4ng3r10us}

## More Information


https://www.w3schools.com/python/ref_random_seed.asp

 - PRNG :
   - https://en.wikipedia.org/wiki/Pseudorandom_number_generator
   - https://www.geeksforgeeks.org/pseudo-random-number-generator-prng/
   - https://www.techtarget.com/whatis/definition/pseudo-random-number-generator-PRNG

 - Substitution :
   - https://bobmckay.com/substituion-cipher-decoding-utility/
