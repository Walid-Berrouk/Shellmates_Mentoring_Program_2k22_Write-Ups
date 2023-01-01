# AES 1

## Description

> I discovered a famous encrpytion and used the simplest mode of it, can you decrypt it ?

## Write-Up

In this challenge we are dealing witn an AES encryption. And since we have the ciper text and the key, all we have to do is to detect the mode and decrypt it.

From the description, we can see that the mode used is the simplest one, so it is obviously the `ECB` mode in 128bits.

We can decrypt it using an online tool like [The X](https://the-x.cn/en-US/cryptography/Aes.aspx) that supports keys in hex format.

## Flag

shellmates{43S_3CB_15_51mpl3}

## More Information

https://www.highgo.ca/2019/08/08/the-difference-in-five-modes-in-the-aes-encryption-algorithm/