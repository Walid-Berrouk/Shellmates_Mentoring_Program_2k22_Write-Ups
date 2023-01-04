# lost byte

## Description

> Oh no! we lost the first byte of this file!!
> 
> Can you still recover it?!

## Write-Up

We we first get the file, we can see that it is broken from its type :

```
└─$ file flag.broken 
flag.broken: data
```

Checking the metadata and inside content, there is no hidden infos or other files.

As the description explains, the file lost it first byte (a part of the magic bytes, which affect its type), so an idea is to recover it by using brute force.

The process will be creating a bunch files, that each file content will be prefixed with a byte from `0x0` to `0xff`. After that, we will check for the files types and see the interesting ones. We will be using the following script :

```py
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
        print()
        imp.write(bytes.fromhex('0' + str(hex(i))[2:]) + content[0] + content[1])
    imp.close()
```

After running it, we will see that the content is prefixed with some content :

```
└─$ cat flag.broken
���`��=
�@▒���=Erd7��V� bnT�H���"�6Z�b��ʗ�a8�#}cmzOɌ~�#JRm�Ĉ�Li#�"�穧}�6�T]�����[������.����fQ,�y1�G�C���"�]QM������Go�<�m(

└─$ cat flag76
L���`��=
�@▒���=Erd7��V� bnT�H���"�6Z�b��ʗ�a8�#}cmzOɌ~�#JRm�Ĉ�Li#�"�穧}�6�T]�����[������.����fQ,�y1�G�C���"�]QM������Go�<�m(
```

So, know we need to check all those files types. To do that, we can run the following script :

```sh
for i in {0..255}; do file "flag$i"; done > res
```

As we check the `res` file, here is one of the files that is compressed :

```
...
flag29: data
flag30: data
flag31: gzip compressed data, last modified: Tue Jun 22 12:12:21 2021, from Unix, original size modulo 2^32 10240
flag32: data
flag33: data
flag34: data
...
```

So, we might need to check its content :

```
cp flag31 flag31.gz
cp flag31 flag31_1
└─$ gzip -d flag31.gz
gzip: flag31 already exists; do you wish to overwrite (y or n)? y
```

From there, we get a new  `tar` file :

```
└─$ file flag31     
flag31: POSIX tar archive (GNU)
```

Let's try to unzip it :

```
tar -xf flag31 
```

We get a plaintext file, the only thing left is to read it.

```
└─$ cat flag.txt   
shellmates{woW_YoU_RECOv3rEd_tHe_fIle!!}
```

**Note :** note that reading the `tar` file display directly its content.

```
└─$ cat flag31 
flag.txt0000664000175000017500000000005114064351617011511 0ustar  malikmalikshellmates{woW_YoU_RECOv3rEd_tHe_fIle!!}
```

## Flag

shellmates{woW_YoU_RECOv3rEd_tHe_fIle!!}

## More Information

 - From hex to bytes in python : https://blog.finxter.com/how-to-convert-hex-string-to-bytes-in-python/
