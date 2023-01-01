# XOR 2

## Description

I've xored my flag using a random key, could you find my secret flag ?

## Write-Up

We continue with `Xor` encryption, but this time with not a property but more of an attack which is : **Known Plain Text Attack**. 

**The known-plaintext attack (KPA)** is an attack model for cryptanalysis where the attacker has access to both the plaintext (called a crib), and its encrypted version (ciphertext). These can be used to reveal further secret information such as secret keys and code books.

In our case, using the `Xor` algorithm, and since we know a part of the flag from the flag format : `shellmates{...}`. We can perfom this attack like following :

We should not forget that:

 - plaintext ⊕ key = encrypted_text
 - encrypted_text ⊕ plaintext = key
 - encrypted_text ⊕ key = plaintext

If the key is smaller than the plaintext, the key is repeated. This fact makes this encryption scheme extremely weak.

In practice, the above equations mean that if we know a part of the initial plaintext, then we can retrieve part of the key relatively easily. By using this partial key we can retrieve a larger part of the plaintext and then a larger part of the key and so forth and so on, till we have accomplished to retrieve the whole key and -as a consequence- the whole plaintext.

So the first thing to do is to apply a `Xor` between the cipher text and the part of the plain text we have.

But, and since the key is random (can be any character even non printables), and the `shellmates` is actually in the middle of the cipherred flag, this means that we should consider making shiftings of the plaintext after repeating it enough time to fit the ciphered text. This way we can ensure that the two parts : `shellmates` of the plain text and the encrypted one actually meets.

**Note :** Note that we can use either `shellmates` or `shellmates` as known plaintext. It should give us the result anyway.

Here is some script to do that :

```py
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
```

As a result, here is what we get for each key :

 - For `shellmates` key :

```py
# keys :
b'shellmatesshellmatesshellmatesshellmatesshellmatesshell'
b'sshellmatesshellmatesshellmatesshellmatesshellmatesshel'
b'esshellmatesshellmatesshellmatesshellmatesshellmatesshe'
b'tesshellmatesshellmatesshellmatesshellmatesshellmatessh'
b'atesshellmatesshellmatesshellmatesshellmatesshellmatess'
b'matesshellmatesshellmatesshellmatesshellmatesshellmates'
b'lmatesshellmatesshellmatesshellmatesshellmatesshellmate'
b'llmatesshellmatesshellmatesshellmatesshellmatesshellmat'
b'ellmatesshellmatesshellmatesshellmatesshellmatesshellma'
b'hellmatesshellmatesshellmatesshellmatesshellmatesshellm'

# key_containers :
b'\xf9~\xa4V\xb1\xf2jj\x94\xfb\xe86\xabI\xf0\xfc9p\xc0\xb3\xfe~\xa8I\xfd\xf6x>\x85\xe0\xf6]\xa3\x15\xe6\xf5F\x1a\x8c\xa7\xe4x\x92\x12\xa2\xe3M\x15\xd4\xa4\xba"\xaeN\xec'
b'\xf9e\xa9_\xb1\xf3f\x7f\x85\xed\xe8-\xa6@\xf0\xfd5e\xd1\xa5\xfee\xa5@\xfd\xf7t+\x94\xf6\xf6F\xae\x1c\xe6\xf4J\x0f\x9d\xb1\xe4c\x9f\x1b\xa2\xe2A\x00\xc5\xb2\xba9\xa3G\xec'
b"\xefe\xb2R\xb8\xf3gs\x90\xfc\xfe-\xbdM\xf9\xfd4i\xc4\xb4\xe8e\xbeM\xf4\xf7u'\x81\xe7\xe0F\xb5\x11\xef\xf4K\x03\x88\xa0\xf2c\x84\x16\xab\xe2@\x0c\xd0\xa3\xac9\xb8J\xe5"
b'\xfes\xb2I\xb5\xfagr\x9c\xe9\xef;\xbdV\xf4\xf44h\xc8\xa1\xf9s\xbeV\xf9\xfeu&\x8d\xf2\xf1P\xb5\n\xe2\xfdK\x02\x84\xb5\xe3u\x84\r\xa6\xeb@\r\xdc\xb6\xbd/\xb8Q\xe8'
b'\xebb\xa4I\xae\xf7nr\x9d\xe5\xfa*\xabV\xef\xf9=h\xc9\xad\xecb\xa8V\xe2\xf3|&\x8c\xfe\xe4A\xa3\n\xf9\xf0B\x02\x85\xb9\xf6d\x92\r\xbd\xe6I\r\xdd\xba\xa8>\xaeQ\xf3'
b'\xe7w\xb5_\xae\xecc{\x9d\xe4\xf6?\xba@\xef\xe20a\xc9\xac\xe0w\xb9@\xe2\xe8q/\x8c\xff\xe8T\xb2\x1c\xf9\xebO\x0b\x85\xb8\xfaq\x83\x1b\xbd\xfdD\x04\xdd\xbb\xa4+\xbfG\xf3'
b'\xe6{\xa0N\xb8\xecxv\x94\xe4\xf73\xafQ\xf9\xe2+l\xc0\xac\xe1{\xacQ\xf4\xe8j"\x85\xff\xe9X\xa7\r\xef\xebT\x06\x8c\xb8\xfb}\x96\n\xab\xfd_\t\xd4\xbb\xa5\'\xaaV\xe5'
b'\xe6z\xac[\xa9\xfaxm\x99\xed\xf72\xa3D\xe8\xf4+w\xcd\xa5\xe1z\xa0D\xe5\xfej9\x88\xf6\xe9Y\xab\x18\xfe\xfdT\x1d\x81\xb1\xfb|\x9a\x1f\xba\xeb_\x12\xd9\xb2\xa5&\xa6C\xf4'
b'\xefz\xadW\xbc\xebnm\x82\xe0\xfe2\xa2H\xfd\xe5=w\xd6\xa8\xe8z\xa1H\xf0\xef|9\x93\xfb\xe0Y\xaa\x14\xeb\xecB\x1d\x9a\xbc\xf2|\x9b\x13\xaf\xfaI\x12\xc2\xbf\xac&\xa7O\xe1'
b'\xe2s\xadV\xb0\xfe\x7f{\x82\xfb\xf3;\xa2I\xf1\xf0,a\xd6\xb3\xe5s\xa1I\xfc\xfam/\x93\xe0\xedP\xaa\x15\xe7\xf9S\x0b\x9a\xa7\xffu\x9b\x12\xa3\xefX\x04\xc2\xa4\xa1/\xa7N\xed'
```

 - For `shellmates{` key :

```py
# keys :
b'shellmates{shellmates{shellmates{shellmates{shellmates{'
b'{shellmates{shellmates{shellmates{shellmates{shellmates'
b's{shellmates{shellmates{shellmates{shellmates{shellmate'
b'es{shellmates{shellmates{shellmates{shellmates{shellmat'
b'tes{shellmates{shellmates{shellmates{shellmates{shellma'
b'ates{shellmates{shellmates{shellmates{shellmates{shellm'
b'mates{shellmates{shellmates{shellmates{shellmates{shell'
b'lmates{shellmates{shellmates{shellmates{shellmates{shel'
b'llmates{shellmates{shellmates{shellmates{shellmates{she'
b'ellmates{shellmates{shellmates{shellmates{shellmates{sh'
b'hellmates{shellmates{shellmates{shellmates{shellmates{s'

# key_containers :
b"\xf9~\xa4V\xb1\xf2jj\x94\xfb\xe0-\xa6@\xf0\xfd5e\xd1\xa5\xfem\xbeM\xf4\xf7u'\x81\xe7\xe0F\xbd\n\xe2\xfdK\x02\x84\xb5\xe3u\x84\x05\xbd\xe6I\r\xdd\xba\xa8>\xaeQ\xfb"
b'\xf1e\xa9_\xb1\xf3f\x7f\x85\xed\xe8%\xbdM\xf9\xfd4i\xc4\xb4\xe8e\xb6V\xf9\xfeu&\x8d\xf2\xf1P\xb5\x02\xf9\xf0B\x02\x85\xb9\xf6d\x92\r\xb5\xfdD\x04\xdd\xbb\xa4+\xbfG\xf3'
b"\xf9m\xb2R\xb8\xf3gs\x90\xfc\xfe-\xb5V\xf4\xf44h\xc8\xa1\xf9s\xbe^\xe2\xf3|&\x8c\xfe\xe4A\xa3\n\xf1\xebO\x0b\x85\xb8\xfaq\x83\x1b\xbd\xf5_\t\xd4\xbb\xa5'\xaaV\xe5"
b'\xefe\xbaI\xb5\xfagr\x9c\xe9\xef;\xbd^\xef\xf9=h\xc9\xad\xecb\xa8V\xea\xe8q/\x8c\xff\xe8T\xb2\x1c\xf9\xe3T\x06\x8c\xb8\xfb}\x96\n\xab\xfdW\x12\xd9\xb2\xa5&\xa6C\xf4'
b'\xfes\xb2A\xae\xf7nr\x9d\xe5\xfa*\xabV\xe7\xe20a\xc9\xac\xe0w\xb9@\xe2\xe0j"\x85\xff\xe9X\xa7\r\xef\xeb\\\x1d\x81\xb1\xfb|\x9a\x1f\xba\xeb_\x1a\xc2\xbf\xac&\xa7O\xe1'
b'\xebb\xa4I\xa6\xecc{\x9d\xe4\xf6?\xba@\xef\xea+l\xc0\xac\xe1{\xacQ\xf4\xe8b9\x88\xf6\xe9Y\xab\x18\xfe\xfdT\x15\x9a\xbc\xf2|\x9b\x13\xaf\xfaI\x12\xca\xa4\xa1/\xa7N\xed'
b'\xe7w\xb5_\xae\xe4xv\x94\xe4\xf73\xafQ\xf9\xe2#w\xcd\xa5\xe1z\xa0D\xe5\xfej1\x93\xfb\xe0Y\xaa\x14\xeb\xecB\x1d\x92\xa7\xffu\x9b\x12\xa3\xefX\x04\xc2\xac\xba"\xaeN\xec'
b'\xe6{\xa0N\xb8\xecpm\x99\xed\xf72\xa3D\xe8\xf4+\x7f\xd6\xa8\xe8z\xa1H\xf0\xef|9\x9b\xe0\xedP\xaa\x15\xe7\xf9S\x0b\x9a\xaf\xe4x\x92\x12\xa2\xe3M\x15\xd4\xa4\xb29\xa3G\xec'
b'\xe6z\xac[\xa9\xfaxe\x82\xe0\xfe2\xa2H\xfd\xe5=w\xde\xb3\xe5s\xa1I\xfc\xfam/\x93\xe8\xf6]\xa3\x15\xe6\xf5F\x1a\x8c\xa7\xecc\x9f\x1b\xa2\xe2A\x00\xc5\xb2\xba1\xb8J\xe5'
b'\xefz\xadW\xbc\xebnm\x8a\xfb\xf3;\xa2I\xf1\xf0,a\xd6\xbb\xfe~\xa8I\xfd\xf6x>\x85\xe0\xfeF\xae\x1c\xe6\xf4J\x0f\x9d\xb1\xe4k\x84\x16\xab\xe2@\x0c\xd0\xa3\xac9\xb0Q\xe8'
b'\xe2s\xadV\xb0\xfe\x7f{\x82\xf3\xe86\xabI\xf0\xfc9p\xc0\xb3\xf6e\xa5@\xfd\xf7t+\x94\xf6\xf6N\xb5\x11\xef\xf4K\x03\x88\xa0\xf2c\x8c\r\xa6\xeb@\r\xdc\xb6\xbd/\xb8Y\xf3'
```

Now, since we have not the key but some bytes that contains inside of them the key, we need to iterate throughout each byte, taking a portion of it that doesn't surpasses the length of the known plaintext we used, and `Xor` it again with our encrypted flag. Note that the right answer with the right flag must contain `shellmates{` string.

Here is some script to do that :

```py
...
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
```

As a result, here is what we get for each key :

 - For `shellmates` key :

```py
# Output
key : b'\xfe~\xa8I\xfd\xf6x>\x85\xe0'
flag :  b'this is the flag :  shellmates{Kn0wn_Pl4in_73xT_4774ck}'
```

 - For `shellmates{` key :


```py
# Output
key : b'\xf9~\xa4V\xb1\xf2jj\x94\xfb\xe0'
flag :  b'shellmates{\xa7\xb0\x81\xca \xaan\xcfTv\xf64[5\xcd\xa8\xb8\x8a\xf9\x11\xce&\x80\xf4<q\xdf\x1b\xbe\xfd\x84\x0c\x9e7\xf0\x887\x00%\xa3 _\xd9`'
key : b'-\xa6@\xf0\xfd5e\xd1\xa5\xfem'
flag :  b'\xa7\xb0\x81\xca \xaan\xcfTv\xf6shellmates{\xe0\x83\xd1k\xe4\x7f\x85B \xcb\xabT,\xd8\xd7\x93\xdc\xb1F\xb5\t\x13\xe3(l\x91L\xe2\xac\x9bn\xdc\xed'
key : b"\xbeM\xf4\xf7u'\x81\xe7\xe0F\xbd"
flag :  b'4[5\xcd\xa8\xb8\x8a\xf9\x11\xce&\xe0\x83\xd1k\xe4\x7f\x85B \xcb\xabshellmates{\xc7\xc7l\xd0\x1b\xceUp\xf0\xb1\xc3p\xc3\xd8\x96\xc4\xf0H\xad+d='
key : b'\n\xe2\xfdK\x02\x84\xb5\xe3u\x84\x05'
flag :  b'\x80\xf4<q\xdf\x1b\xbe\xfd\x84\x0c\x9eT,\xd8\xd7\x93\xdc\xb1F\xb5\t\x13\xc7\xc7l\xd0\x1b\xceUp\xf0\xb1\xc3shellmates{\xc4l\xd1*\xb3S|\xa9\xbe\xa6\x85'
key : b'\xbd\xe6I\r\xdd\xba\xa8>\xaeQ\xfb'
flag :  b'7\xf0\x887\x00%\xa3 _\xd9`\xe3(l\x91L\xe2\xac\x9bn\xdc\xedp\xc3\xd8\x96\xc4\xf0H\xad+d=\xc4l\xd1*\xb3S|\xa9\xbe\xa6\x85shellmates{'
key : b'\xfe~\xa8I\xfd\xf6x>\x85\xe0'
flag :  b'this is the flag :  shellmates{Kn0wn_Pl4in_73xT_4774ck}'
```

So we get the key and the flag (The most readable one).

**Note 1 :** Note that is was better to use `shellmates` as plain text then use `shellmates{` as a verification bytes for the flag. Sometimes, it is impirative to use the second one for both, sometimes not like in our case. So just test them both !

**Note 2 :** The decryption is the encryption itself (Which is a Xor), we can use also xor method from pwn.


## Flag

shellmates{Kn0wn_Pl4in_73xT_4774ck}

## More Information

his tool contains the most common two types of attack [Known-Plaintext Attack , Many Time Pad Attack] for Xor encryption : https://github.com/X-Vector/X0R
Known plaintext attack on Xor explained : https://alamot.github.io/xor_kpa/