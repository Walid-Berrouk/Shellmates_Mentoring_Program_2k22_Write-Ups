#! /usr/bin/python3


# imp.write(b'aaaabcaab\x13\x12\x00\x00')

flag_broken = open('flag.broken', 'rb')
content = flag_broken.readlines()

for i in range(0xff + 0x01) :
    imp = open(f'flag{i}', 'wb')
    # print(str(hex(i))[2:])
    if i > 0xf :
        imp.write(bytes.fromhex(str(hex(i))[2:]) + content[0] + content[1])
    else :
        imp.write(bytes.fromhex('0' + str(hex(i))[2:]) + content[0] + content[1])
    imp.close()