# inspect-me

## Description

> Inspect me plz

## Write-Up

A Classic inspect me challenge, where you access the website and then, using the console, inspect the html content.

Or just fetch all the page in your terminal using `curl` :

```
curl 'http://inspect-me.web_client.challs.ctf.shellmates.club/'
```


```html
<!DOCTYPE html>
<html>
    <head>
        <title>Inspect Me</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" />
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js"></script>
        <style>
          .container {
            height: 10vh;
            display: flex;
            justify-content: center;
            align-items: center;
          }
        </style>
    </head>

    <body>
      <div class="container">
        <h1>Nothing to see here</h1>
      </div>
      <!-- shellmates{CLA$SI1111C_ch4l1enGE} -->
    </body>
</html>
```

## Flag

shellmates{CLA$SI1111C_ch4l1enGE}