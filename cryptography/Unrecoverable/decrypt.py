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

# Output
# abcdefghijklmnopqrstuvwxyz0123456789
# mr02n3ytwjl4vsd6qxcue5kh981gfoazipb7

dec = ""
for i in flag_enc:
    if i.isalnum():
        # shuffles only if alphanumeric (ecip, unshuffle only if alphanumeric)
        dec += chars[shuffled_chars.index(i)]
    else:
        dec += i

print(dec)

# Output
# shellmates{f1x1ng_th3_s33d_1s_d4ng3r10us}