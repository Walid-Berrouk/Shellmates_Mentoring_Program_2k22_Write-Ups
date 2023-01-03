# machines

## Description

> I hide my flag in places that no one can find.

## Write-Up

When accessing the website, we can see some star wars background as well as refers to its robots `C3PO` and `R2D2`.

And from the title of the challenge as well, we may wanna check `robots.txt` file of this website :

```
curl 'http://machines.web-client.challs.ctf.shellmates.club/robots.txt'
```

```
User-Agent: *
Disallow: /s333333333cr3t   
```

As we can see, there is a hidden route which is `/s333333333cr3t`, so let's check it out :

```
curl 'http://machines.web-client.challs.ctf.shellmates.club/s333333333cr3t'
```

```
<h3>can't even hide my secrets any more :/</h3> <h3>shellmates{beep_b00p_beep_b3ep_?}<h3>  
```

## Flag

shellmates{beep_b00p_beep_b3ep_?}