# just /bin/bash

## Description

> Yaaay I got a shell!
> Wait there's no ls, no cat, just /bin/bash !!

## Write-Up

After accessing the instance, and from the description, we can't execute neither `ls` nor `cat` commands. So first thing we do is check for available commands, aliases and symboles we have in this bash :

```
compgen -ac
```

```
if
then
else
elif
fi
case
esac
for
select
while
until
do
done
in
function
time
{
}
!
[[
]]
coproc
.
:
[
alias
bg
bind
break
builtin
caller
cd
command
compgen
complete
compopt
continue
declare
dirs
disown
echo
enable
eval
exec
exit
export
false
fc
fg
getopts
hash
help
history
jobs
kill
let
local
logout
mapfile
popd
printf
pushd
pwd
read
readarray
readonly
return
set
shift
shopt
source
suspend
test
times
trap
true
type
typeset
ulimit
umask
unalias
unset
wait
bash
```

As we can see, `echo` is available :

```
-bash-5.1$ echo 'hello'
hello
```

So let's try to use it to `ls` folder and `cat` files :

```
-bash-5.1$ echo */*
bin/bash lib/x86_64-linux-gnu lib64/ld-linux-x86-64.so.2
-bash-5.1$ echo *
bin flag.txt lib lib64
```

Let's read `flag.txt` then :

```
-bash-5.1$ echo "$(<flag.txt)"
shellmates{sH3ll_built1ns_FTW}
```

**Trick Move :** you can output the file content with an execution error :

```
-bash-5.1$ . flag.txt
-bash: shellmates{sH3ll_built1ns_FTW}: command not found
```

## Flag

shellmates{sH3ll_built1ns_FTW}

## More Information

Alternatives of `ls` commad : https://ubunlog.com/en/alternatives-to-ls-command/
Read file without cat : 
 - https://unix.stackexchange.com/questions/63658/redirecting-the-content-of-a-file-to-the-command-echo
 - https://jarv.org/posts/cat-without-cat/
