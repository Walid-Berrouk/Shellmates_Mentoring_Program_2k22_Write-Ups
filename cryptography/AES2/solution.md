# AES 2

## Description

> For this time, I used more complex mode, you can't get over it

## Write-Up

In this challenge we are dealing witn an AES encryption. And since we have the ciper text and the key, all we have to do is to detect the mode and decrypt it.

From the description, we can see that the mode used is a complexx one, so we can try the others starting with `CBC` mode in 128bits, and indeed, it used `CBC` mode in 128 bits.

We can decrypt it using an online tool like [The X](https://the-x.cn/en-US/cryptography/Aes.aspx) that supports keys and IVs in hex format.

## Flag

shellmates{3v3n_CBC_m0d3_c4n't_st0p_m3}

## More Information

https://www.highgo.ca/2019/08/08/the-difference-in-five-modes-in-the-aes-encryption-algorithm/    