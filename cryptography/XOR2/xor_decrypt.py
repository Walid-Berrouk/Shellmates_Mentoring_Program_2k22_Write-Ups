#!/usr/bin/python3

from pwn import xor

flag = b'\x8a\x16\xc1:\xdd\x9f\x0b\x1e\xf1\x88\x9b^\xce%\x9c\x91X\x04\xa5\xc0\x8d\x16\xcd%\x91\x9b\x19J\xe0\x93\x855\xc6y\x8a\x98\'n\xe9\xd4\x97\x10\xf7~\xce\x8e,a\xb1\xd7\xc9J\xcb"\x80'

# key = b'shellmates{'
key = b'shellmates'

# key_fit = key*5
key_fit = key*6

key_containers = []

for i in range(len(key)) :
    key_container = xor(flag, key_fit[:len(flag)])
    key_containers.append(xor(flag, key_fit[:len(flag)]))

    # print(key_container)
    # print(key_containers)

    key_fit = chr(key[(len(key) - 1) - i]).encode() + key_fit
    # print(key_fit[:len(flag)])

for key_container in key_containers :
    for length in range(1, len(key) + 1) :
        for i in range(len(key_container)) :
            try :
                flag_decrypted = xor(flag, key_container[i : i + length])
                if b'shellmates{' in flag_decrypted :
                    print("key :", key_container[i : i + length])
                    print("flag : ", flag_decrypted)
            except :
                continue