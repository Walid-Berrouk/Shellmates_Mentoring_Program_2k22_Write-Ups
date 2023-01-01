# 652AHS

## Description

> I read that hashing algorithms are irreversible, so I hashed my password and forgot it, can you recover it for me ? (Put the password in the flag format shellmates{...})

## Write-Up

From the Title and description of the challenge, we can easily deduce that the string given in the `hash.txt` file is actually a `sha256` hash. So let's try to decrypt it using some online tools like :

 - https://crackstation.net/
 - https://md5decrypt.net/en/Sha256/


After decrypting it, we get the following passord : `300489`

So, all we have to do is to wrap it in the flag format.


## Flag

shellmates{300489}

## More Information